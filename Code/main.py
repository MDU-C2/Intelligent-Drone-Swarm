import time
import numpy as np
import pybullet as p
import controller
from gym_pybullet_drones.FLA402.env import SearchAreaAviary
from gym_pybullet_drones.FLA402.searchArea import SearchArea
from gym_pybullet_drones.FLA402.drone import Drone
from gym_pybullet_drones.FLA402.avoidance import avoidance_from_drones
from gym_pybullet_drones.FLA402.avoidance import avoidance_from_borders
from gym_pybullet_drones.FLA402.avoidance import get_all_positions
from gym_pybullet_drones.FLA402.retasking import RetaskingSystem
from gym_pybullet_drones.FLA402.tables import get_all_health_codes, get_health_name
from gym_pybullet_drones.FLA402.market import MarketSystem

#NUM_D
# RONES = 4
HOME_POSITION = (0, 0)
FLY_HEIGHT = 1.0
SECTION_SWEEP_STEPS = 4
SEARCH_OFFSET = (6, 4)

WAYPOINT_TOLERANCE = 0.10
HOVER_TIME = 0.2
MAX_SPEED = 6.0
CTRL_FREQ = 60
BROADCAST_PERIOD = 5.0  # seconds
RETURN_TIMEOUT = 10.0                   
# return_timeout is the time before sections are released from the drone returning home. It will act like a timeout for a drone returning home since soemthing can happen to a drone while returning home.

def generate_drone_positions(num_agents, radius, home_xy):
    #in this function, we define position the drones will spawn in
    positions = []
    for i in range(num_agents):
        angle = (2 * np.pi / num_agents) * i
        x = home_xy[0] + radius * np.cos(angle)
        y = home_xy[1] + radius * np.sin(angle)
        z = 0.03
        positions.append([x, y, z])
    return np.array(positions)

def generate_lawnmower_points(center, section_size, steps):
    #Generate lawn-mower pattern fully inside each sectio.
    cx, cy = center
    half = section_size / 2
    margin = 0.30 * section_size   # a margine of 30% so that the drones don't need to be exactly at the edge/line of the section.
    x1, x2 = cx - half + margin, cx + half - margin
    y1, y2 = cy - half + margin, cy + half - margin
    ys = np.linspace(y1, y2, steps)
    pts = []
    flip = False # acts like a switch for the drone to go from (x1 → x2) when False and then (x2 → x1) when True and etc.
    for y in ys:
        if not flip:
            pts += [(x1, y, FLY_HEIGHT), (x2, y, FLY_HEIGHT)]
        else:
            pts += [(x2, y, FLY_HEIGHT), (x1, y, FLY_HEIGHT)]
        flip = not flip
    return pts

def rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents):
    
    for drone_id in range(num_agents):
        owned = [s for s in market.sections if s["owner"] == drone_id and not s["searched"]]
        if not owned:
            drone_tasks[drone_id] = iter([])
            continue

        drone_xy = np.array(swarm[drone_id].position)[:2]
        owned.sort(key=lambda s: np.linalg.norm(drone_xy - s["pos"][:2]))

        paths = []
        for sec in owned:
            path = generate_lawnmower_points(sec["pos"], area.section_size, SECTION_SWEEP_STEPS)
            paths.append((sec["id"], path))
        drone_tasks[drone_id] = iter(paths)

def main(num_agents = 4):
    start_time = time.time()
    print("Initializing environment...")
    initial_xyz_agent = generate_drone_positions(num_agents, 0.4, HOME_POSITION)
    env = SearchAreaAviary(
        num_drones=num_agents,
        initial_xyzs=initial_xyz_agent,
        gui=True,
        grid_size=(3, 3),
        section_size=1.5,
        home_position=(0, 0),
        search_area_offset=(6, 4)
    )

    area = SearchArea(grid_size=(3, 3), section_size=1.5, home=SEARCH_OFFSET)

    swarm = [Drone(i, env, initial_xyz_agent[i]) for i in range(num_agents)]
    market = MarketSystem(num_agents, area)
    market_initialized = False
    drone_tasks = {i: iter([]) for i in range(num_agents)}
    return_timer = [0.0] * num_agents       # countdown for drones sent home
    return_active = [False] * num_agents    # whether that drone’s timer is running

    print("Mission started. drones searching assigned sections...")
    current_targets = [None] * num_agents
    path_progress = [0] * num_agents
    last_reach_time = [0] * num_agents
    current_section = [None] * num_agents
    last_broadcast = [0.0] * num_agents

    returning_home = False
    home_targets = generate_drone_positions(num_agents, 0.4, HOME_POSITION)
    crashed = [False] * num_agents
    crash_timer = [0.0] * num_agents

    retasker = RetaskingSystem(home_targets)
    # Example: a per-drone health list (all OK initially)
    health_status = [0] * num_agents  # 0 = OK

    if not hasattr(controller, "injected_fault"):
        controller.injected_fault = None

    while True:
        t = time.time() - start_time #we need - start_time so that the timer starts at 0 when the "start mission" is pressed and not when start simulation.
        actions = np.zeros((num_agents, 4)) # 4 representing the amount of propellers. This will create a matrix with number of agents as row and 4 columns where each cell will contain rpm for each motor.
        # get current positions of all drones for avoidance calculations
        all_positions = get_all_positions(env, num_agents)

        # Check for injected fault from GUI 
        if controller.injected_fault:
            fault_drone, fault_code = controller.injected_fault
            health_status[fault_drone] = fault_code
            controller.injected_fault = None  # reset
            fault_name = get_health_name(fault_code)
            print(f"[GUI Inject] agent {fault_drone} fault set to {fault_name}")


         # abort 
        if controller.mission_aborted:
            returning_home = True
            controller.mission_aborted = False
            print("GUI: Mission abort detected, returning home!")

        if not controller.search_active and not returning_home:
            time.sleep(0.1)
            continue

        # First tick after Start Search: open market once, build tasks
        if not market_initialized:
            drone_positions = [drone.position for drone in swarm]
            market.open_market(drone_positions)
            controller.market_text = market.get_market_status()

            rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents)
            
            market_initialized = True

        for i, drone in enumerate(swarm):
            state = drone.update()
            current_pos = np.array(state[0:3])
            
            # --- Retasking / fault handling ---
            if health_status[i] != 0:  # non-OK health
                result = retasker.handle(i, health_status[i])
                if result:
                    action = result["action"]

                    if action in ("RETURN_HOME"):
                        # fly back home smoothly
                        target_pos = np.array(home_targets[i])
                        diff = target_pos - current_pos
                        dist = np.linalg.norm(diff)
                        if dist > 0.05:
                            next_pos = current_pos + 0.3 * diff  # move toward home
                        else:
                            next_pos = target_pos

                        rpm = drone.step_toward(next_pos)
                        actions[i, :] = rpm
                        
                        if not return_active[i]:
                            return_active[i] = True
                            return_timer[i] = time.time()
                            print(f"Agent {i} returning home — market release countdown started.")
                        continue  # skip normal search

                    elif action == "LAND_NOW":
                        # Emergency land at current spot
                        target_pos = np.array([current_pos[0], current_pos[1], 0.05])
                        next_pos = current_pos + 0.2 * (target_pos - current_pos)
                        rpm = drone.step_toward(next_pos)
                        actions[i, :] = rpm

                        # --- Release this drone's sections back to the market ---
                        market.release_drone_sections(i)
                        controller.market_text = market.get_market_status()

                        # --- Trigger dynamic rebuy for other drones ---
                        drone_positions = [d.position for d in swarm]
                        market.dynamic_update(drone_positions)
                        controller.market_text = market.get_market_status()

                        # --- Rebuild tasks to reflect new market ownership ---
                        rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents)

                        controller.middle_text = f"Agent {i} emergency landed — sections returned to market."
                        continue  # skip search logic for this drone

                    elif action in ("HOVER", "REDUCED_ROLE", "HOVER_AND_RECONNECT"):
                        # just hover high up so that it can be used as a relay but not disturb other drones when searching.
                        target_pos = np.array([current_pos[0], current_pos[1], 2])
                        next_pos = current_pos + 0.2 * (target_pos - current_pos)
                        rpm = drone.step_toward(next_pos)                        
                        actions[i, :] = rpm

                         # --- Release this drone's sections back to the market ---
                        market.release_drone_sections(i)
                        controller.market_text = market.get_market_status()

                        # --- Trigger dynamic rebuy for other drones ---
                        drone_positions = [d.position for d in swarm]
                        market.dynamic_update(drone_positions)
                        controller.market_text = market.get_market_status()
                        
                        controller.middle_text = f"Agent {i} is being used as a relay, sections returned to market."
                        continue

            # --- Detect crash (persistent) ---
            if not crashed[i]:
                if current_pos[2] <= 0.1:  # near ground
                    if crash_timer[i] == 0.0:
                        crash_timer[i] = time.time()
                    elif time.time() - crash_timer[i] > 6.0:  # stayed low for >6s
                        crashed[i] = True
                        print(f"drone {i} has crashed! Altitude={current_pos[2]:.2f}")
                        p.addUserDebugText(
                            "CRASHED",
                            [current_pos[0], current_pos[1], 0.1],
                            textColorRGB=[1, 0, 0],
                            textSize=2,
                            lifeTime=0,
                            physicsClientId=env.CLIENT
                        )

                         # --- Release this drone's sections back to the market ---
                        market.release_drone_sections(i)
                        controller.market_text = market.get_market_status()

                        # --- Trigger dynamic rebuy for other drones ---
                        drone_positions = [d.position for d in swarm]
                        market.dynamic_update(drone_positions)
                        controller.market_text = market.get_market_status()

                        continue  # skip all control for this drone
                else:
                    crash_timer[i] = 0.0
            else:
                continue  # permanently skip control once marked crashed

           # Broadcast every 5 seconds
            if t - last_broadcast[i] >= BROADCAST_PERIOD:
                msg = drone.broadcast()  # uses drone.broadcast()
                print(f"[Ping] drone {msg['ID']} at {msg['Pos']} | Time: {msg['Timer']}s")
                last_broadcast[i] = t

            # --- Return-home behavior ---
            if returning_home:
                target_pos = np.array([home_targets[i][0], home_targets[i][1], FLY_HEIGHT])
                diff = target_pos - current_pos
                dist = np.linalg.norm(diff)
                if dist > 0.05:
                    next_pos = current_pos + diff * 0.3  # smooth flight home
                else:
                    next_pos = target_pos
                rpm = drone.step_toward(next_pos)
                actions[i, :] = rpm
                continue

            # --- Normal search behavior ---
            if current_targets[i] is None:
                try:
                    cell_id, path = next(drone_tasks[i])
                except StopIteration:
                    # No more tasks -> hover and wait
                    hover_target = np.array([current_pos[0], current_pos[1], FLY_HEIGHT])
                    rpm = drone.step_toward(hover_target)
                    actions[i, :] = rpm
                    continue

                current_targets[i] = path
                path_progress[i] = 0
                current_section[i] = cell_id
                last_reach_time[i] = time.time()  # prevent initial hover pause
                print(f"drone {i} → new section {cell_id}")

            # If drone has finished its tasks, just hover and wait
            if current_targets[i] is None:
                hover_target = np.array([current_pos[0], current_pos[1], FLY_HEIGHT])
                rpm = drone.step_toward(hover_target)
                actions[i, :] = rpm
                continue

            target_pos = current_targets[i][path_progress[i]]
            diff = np.array(target_pos) - current_pos
            dist = np.linalg.norm(diff)
            direction = diff / (dist + 1e-6)
            speed_scale = np.clip(dist / 3.0, 0.5, 2.0)
            move_dist = min(dist, MAX_SPEED * speed_scale / CTRL_FREQ * 2)
            next_pos = current_pos + direction * move_dist

                    # --- Apply potential-field avoidance ---
            push_drones = avoidance_from_drones(current_pos, all_positions, i,
                                            radius=0.5, gain=0.4, max_push=0.6)
            push_border = avoidance_from_borders(current_pos, (3, 3), 1.5, (6, 4),
                                             margin=0.3, gain=0.6, max_push=0.6)
            next_pos = next_pos + 0.5 * (push_drones + push_border)
            
            if int(t) % 60 == 0:
                drone.controller.reset()
            
            next_pos[2] = FLY_HEIGHT

            rpm =drone.step_toward(next_pos)
            actions[i, :] = rpm

            if dist < WAYPOINT_TOLERANCE:
                if time.time() - last_reach_time[i] > HOVER_TIME:
                    path_progress[i] += 1
                    last_reach_time[i] = time.time()
                    if path_progress[i] >= len(current_targets[i]):
                        area.mark_searched(current_section[i])
                        print(f"drone {i} finished section {current_section[i]}")

                        # 1) reward and remove from market
                        market.reward_and_remove_section(i, current_section[i])
                        controller.market_text = market.get_market_status()

                        # 2) let market re-allocate any available sections
                        drone_positions = [d.position for d in swarm]
                        market.dynamic_update(drone_positions)
                        controller.market_text = market.get_market_status()

                        # 3) rebuild all drones' task iterators from current market ownership
                        rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents)

                        # 4) IMMEDIATELY try to assign a new section to THIS drone
                        current_targets[i] = None
                        path_progress[i] = 0
                        last_reach_time[i] = time.time()

                        try:
                            cell_id, path = next(drone_tasks[i])   # pull a fresh section now
                            current_section[i] = cell_id
                            current_targets[i] = path
                            # (no hover — we will fly to it right away)
                        except StopIteration:
                            # nothing to do right now — hover this frame
                            hover_target = np.array([current_pos[0], current_pos[1], FLY_HEIGHT])
                            rpm = drone.step_toward(hover_target)
                            actions[i, :] = rpm
                            continue


        # --- Update GUI displays via controller ---
        broadcast_lines = []
        for i, drone in enumerate(swarm):
            msg = drone.broadcast()
            broadcast_lines.append(
                f"Agnet {msg['ID']}: Pos={tuple(np.round(msg['Pos'],2))}, Time={msg['Timer']}s"
            )
        controller.broadcast_text = "\n".join(broadcast_lines)

        assign_lines = []
        for i in range(num_agents):
            sections = [c.id for c in area.sections if c.assigned_drone == i]
            assign_lines.append(f"drone {i}: Sections {sections}")
        controller.assignment_text = "\n".join(assign_lines)

                # --- Update searched sections display ---
        searched_lines = []
        for c in area.sections:
            status = "✅ Done" if c.searched else "🔲 Searching"
            searched_lines.append(f"Section {c.id}: {status}")
        controller.searched_text = "\n".join(searched_lines)

        # --- Handle drones that went home (timeout → release sections) ---
        for j in range(num_agents):
            if return_active[j]:
                if time.time() - return_timer[j] >= RETURN_TIMEOUT:
                    print(f"drone {j}'s return-home timeout reached — releasing owned sections.")
                    return_active[j] = False
                    market.release_drone_sections(j)
                    controller.market_text = market.get_market_status()

                    # allow other drones to buy them
                    drone_positions = [d.position for d in swarm]
                    market.dynamic_update(drone_positions)
                    controller.market_text = market.get_market_status()
                    rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents)

        env.step(actions)
        time.sleep(1 / CTRL_FREQ)

        # --- Check if all sections are searched ---
        if all(c.searched for c in area.sections) and not returning_home:
            print("The search area is searched! drones will return home together...")
            returning_home = True
            time.sleep(1.5)  # small pause before returning

        if returning_home:
            distances = []
            for i in range(num_agents):
                if crashed[i]:
                    continue #here we are skipping a crashed drone
                pos = np.array(env._getDroneStateVector(i)[0:3])
                dist = np.linalg.norm(pos[:2] - home_targets[i][:2])
                distances.append(dist)
            

            if len(distances) == 0 or all(d < 0.2 for d in distances):  # ← inside same block now
                print("All drones returned home. Mission complete!")
                 # Gradually descend to z=0

                for _ in range(int(CTRL_FREQ * 30)):  # ~30 seconds descent
                    actions = np.zeros((num_agents, 4))
                    for i, drone in enumerate(swarm):
                        if crashed[i]:
                            continue
                        state = drone.update()
                        current_pos = np.array(state[0:3])
                        target_pos = np.array([home_targets[i][0], home_targets[i][1], 0.05])  # near ground
                        next_pos = current_pos + 0.2 * (target_pos - current_pos)
                        rpm = drone.step_toward(next_pos)
                        actions[i, :] = rpm
                    env.step(actions)
                    time.sleep(1 / CTRL_FREQ)

                print("All functioning drones landed (z≈0). Mission complete.")
                controller.search_active = False
                controller.simulation_running = False
                break

if __name__ == "__main__":
    main()
