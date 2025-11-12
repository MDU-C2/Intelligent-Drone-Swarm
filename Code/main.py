import time
import numpy as np
import pybullet as p
import controller
import sys
from gym_pybullet_drones.FLA402.env import SearchAreaAviary
from gym_pybullet_drones.FLA402.searchArea import SearchArea
from gym_pybullet_drones.FLA402.drone import Drone
from gym_pybullet_drones.FLA402.avoidance import avoidance_from_drones
from gym_pybullet_drones.FLA402.avoidance import avoidance_from_borders
from gym_pybullet_drones.FLA402.avoidance import get_all_positions
from gym_pybullet_drones.FLA402.retasking import RetaskingSystem
from gym_pybullet_drones.FLA402.tables import get_health_name
from gym_pybullet_drones.FLA402.market import MarketSystem
from gym_pybullet_drones.FLA402.subject import SubjectManager
from gym_pybullet_drones.FLA402.subject import SubjectManager

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

def generate_drone_positions(num_agents, home_xy):

    # Adaptive radius: increases slowly with sqrt(N)
    radius = 0.8 + 0.25 * np.sqrt(num_agents)
    positions = []
    for i in range(num_agents):
        angle = (2 * np.pi / num_agents) * i
        x = home_xy[0] + radius * np.cos(angle)
        y = home_xy[1] + radius * np.sin(angle)
        z = 0.03
        positions.append([x, y, z])
    return np.array(positions), radius

    
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

def main(num_agents = 4, grid_size = 4):
    start_time = time.time()
    print("Initializing environment...")
    initial_xyz_agent, formation_radius = generate_drone_positions(num_agents, HOME_POSITION)

    # Since there was a problem with the grid comming to close to home pad when it gets bigger, we need to increase the grid offset based on grid size.
    offset_x = 4 + 1.0 * formation_radius + 0.75 * grid_size 
    offset_y = 2 + 0.5 * formation_radius + 0.5 * grid_size

    env = SearchAreaAviary(
        num_drones=num_agents,
        initial_xyzs=initial_xyz_agent,
        gui=True,
        grid_size=(grid_size, grid_size),
        section_size=1.5,
        home_position=(0, 0),
        search_area_offset=(offset_x, offset_y),
        helipad_radius=formation_radius 
    )

    

    charged_complete = [False] * num_agents  # True once the drone has been charged successfully
    search_offset = (offset_x, offset_y)
    area = SearchArea(grid_size=(grid_size, grid_size), section_size=1.5, home=search_offset)

    # After area and env initialization
    subject_mgr = SubjectManager(env, area, urdf_path=r"C:\Users\yonat\gym-pybullet-drones\gym_pybullet_drones\FLA402\human_urdf\human_urdf\unnamed\urdf\unnamed.urdf")
    subject_pos = subject_mgr.spawn_random_subject()
    # Spawn subject
    subject_found = False
    voting_active = False
    verification_targets = {}   # which drones fly where during voting
    votes = []
    helpers = []

    return_reason = [""] * num_agents   # reason for returning home
    battery_return_start = {}           # tracks timestamp when battery-change started
    battery_late = set()                # drones that exceeded 1 min charge time

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
    home_targets, _ = generate_drone_positions(num_agents, HOME_POSITION)
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

                # --- Battery change timeout: if >60s at home without charge, release sections ---
        for j in range(num_agents):
            if return_reason[j] == "battery" and not charged_complete[j]:
                if j in battery_return_start and (time.time() - battery_return_start[j]) > 60.0:
                    if j not in battery_late:
                        print(f"[Battery Timeout] Drone {j} took too long to change battery. Releasing sections.")
                        battery_late.add(j)
                        market.release_drone_sections(j)
                        controller.market_text = market.get_market_status()

                        # Allow others to rebuy
                        drone_positions = [d.position for d in swarm]
                        market.dynamic_update(drone_positions)
                        controller.market_text = market.get_market_status()
                        rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents)


        for i, drone in enumerate(swarm):
            state = drone.update()
            current_pos = np.array(state[0:3])

            if (
                not subject_found
                and not voting_active
                and not returning_home
                and controller.search_active
                and current_section[i] is not None
                and subject_pos is not None
                and t > 20
            ):

                drone_xy = np.array(current_pos[:2])
                subject_xy = np.array(subject_pos[:2])
                dist_to_subject = np.linalg.norm(drone_xy - subject_xy)


                if dist_to_subject < 0.4:
                    subject_found = True
                    drone.subject_found = 1
                    controller.middle_text = (
                        f"Drone {i} detected possible subject at {np.round(subject_pos[:2], 2)}!"
                    )
                    print(controller.middle_text)

                    # Choose 3 closest helper drones
                    dists = [
                        (j, np.linalg.norm(
                            np.array(swarm[j].position[:2]) - np.array(subject_pos[:2])
                        ))
                        for j in range(num_agents) if j != i
                    ]
                    dists.sort(key=lambda x: x[1])
                    helpers = [idx for idx, _ in dists[:3]]
                    print(f"[Subject] Drones {helpers} assigned to verify subject")

                    controller.voting_text = (
                        "Subject verification started\n"
                        f"Candidate position: {np.round(subject_pos[:2], 2)}\n"
                        f"Verifiers: {helpers}\n"
                    )

                    # Assign verification targets around the subject
                    verification_targets = {}
                    angles = [0, 120, 240]
                    for k, drone_id in enumerate(helpers):
                        # NEW (targets at hover z)
                        offx = np.cos(np.radians(angles[k])) * 0.5
                        offy = np.sin(np.radians(angles[k])) * 0.5
                        verification_targets[drone_id] = np.array([subject_pos[0] + offx,
                                                                subject_pos[1] + offy,
                                                                FLY_HEIGHT])
                    voting_active = True
                    votes = []


            if i in controller.charged_drones:
                print(f"[MAIN] Drone {i} recharged — rejoining mission.")
                controller.charged_drones.remove(i)
                health_status[i] = 0
                controller.home_ready[i] = False
                charged_complete[i] = True
                battery_return_start.pop(i, None)  # clear battery timer
                return_reason[i] = ""              # reset reason


                if i in battery_late:
                    print(f"[Penalty] Drone {i} took too long to charge. Must buy section (cost 2 points).")
                    # Apply penalty and force market purchase ignoring distance
                    market.force_buy_section(i, cost=2)
                    battery_late.remove(i)
                else:
                    # Normal return: resume with previous sections if any
                    drone_positions = [d.position for d in swarm]
                    market.dynamic_update(drone_positions)

                controller.market_text = market.get_market_status()
                rebuild_tasks_from_market(drone_tasks, market, area, swarm, num_agents)
                continue

            # --- Retasking / fault handling ---
            if health_status[i] != 0:  # non-OK health
                result = retasker.handle(i, health_status[i])
                if result:
                    action = result["action"]

                    if action in ("RETURN_HOME"):
                        target_pos = np.array(home_targets[i])
                        diff = target_pos - current_pos
                        dist = np.linalg.norm(diff)
                        if dist > 0.05:
                            next_pos = current_pos + 0.3 * diff
                        else:
                            next_pos = target_pos
                        rpm = drone.step_toward(next_pos)
                        # --- Detect if drone reached home (close enough) ---
                        if dist < 0.2:  # within 20 cm of home pad
                            controller.home_ready[i] = True
                        else:
                            controller.home_ready[i] = False

                        actions[i, :] = rpm

                        if not return_active[i]:
                            return_active[i] = True
                            return_timer[i] = time.time()
                            charged_complete[i] = False
                            return_reason[i] = "battery"
                            battery_return_start[i] = time.time()
                            print(f"Agent {i} returning home for battery change.")
                        continue


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

           #return home
            if returning_home:
                for i, drone in enumerate(swarm):
                    if crashed[i]:
                        continue

                    state = drone.update()
                    current_pos = np.array(state[0:3])
                    target_pos = np.array([home_targets[i][0], home_targets[i][1], FLY_HEIGHT])
                    diff = target_pos - current_pos
                    dist = np.linalg.norm(diff)

                    if dist > 0.05:
                        direction = diff / (dist + 1e-6)
                        speed_scale = np.clip(dist / 3.0, 0.3, 1.0)
                        move_dist = min(dist, MAX_SPEED * speed_scale / CTRL_FREQ * 6)
                        next_pos = current_pos + direction * move_dist
                    else:
                        next_pos = target_pos

                    next_pos[2] = FLY_HEIGHT
                    rpm = drone.step_toward(next_pos)
                    actions[i, :] = rpm

                env.step(actions)
                time.sleep(1 / CTRL_FREQ)
                continue  # skip normal mission logic during return phase


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

            # --- Voting phase ---
            if voting_active:
                for j in verification_targets.keys():
                    target = verification_targets[j]

                    # --- XY-only distance (ignore z) ---
                    diff_xy = target[:2] - swarm[j].position[:2]
                    dist = np.linalg.norm(diff_xy)

                    if dist > 0.25:  # tolerance for "in position"
                        # Smooth, faster approach but stable
                        direction = diff_xy / (dist + 1e-6)
                        # faster than before; tune 1.2–2.0 as you like
                        move_dist = min(dist, MAX_SPEED / CTRL_FREQ * 1.6)
                        next_xy = swarm[j].position[:2] + direction * move_dist
                        next_pos = np.array([next_xy[0], next_xy[1], FLY_HEIGHT])
                        rpm = swarm[j].step_toward(next_pos)
                        actions[j, :] = rpm
                    else:
                        # Register vote once
                        if j not in [v["drone_id"] for v in votes]:
                            votes.append({"drone_id": j, "vote": "YES"})
                            msg = f"Drone {j} votes YES at {np.round(swarm[j].position[:2], 2)}"
                            print(msg)
                            controller.voting_text += msg + "\n"

                        # Hold a stable hover after voting
                        hover_target = np.array([swarm[j].position[0], swarm[j].position[1], FLY_HEIGHT])
                        rpm = swarm[j].step_toward(hover_target)
                        actions[j, :] = rpm


                # ✅ Continue normal search for *other drones*
                for k in range(num_agents):
                    if k not in verification_targets and not crashed[k]:
                        # Only run search if they have targets
                        if current_targets[k] is not None and path_progress[k] < len(current_targets[k]):
                            target_pos = current_targets[k][path_progress[k]]
                            diff = np.array(target_pos) - swarm[k].position
                            dist = np.linalg.norm(diff)
                            direction = diff / (dist + 1e-6)
                            move_dist = min(dist, MAX_SPEED / CTRL_FREQ)
                            next_pos = swarm[k].position + direction * move_dist

                            # Apply light avoidance
                            push_drones = avoidance_from_drones(
                                swarm[k].position, all_positions, k, radius=0.5, gain=0.3, max_push=0.4
                            )
                            push_border = avoidance_from_borders(
                                swarm[k].position, (grid_size, grid_size), 1.5, search_offset,
                                margin=0.3, gain=0.5, max_push=0.4
                            )
                            next_pos += 0.5 * (push_drones + push_border)
                            next_pos[2] = FLY_HEIGHT

                            rpm = swarm[k].step_toward(next_pos)
                            actions[k, :] = rpm
                        
                            # Advance waypoint if close
                            if dist < WAYPOINT_TOLERANCE:
                                if time.time() - last_reach_time[k] > HOVER_TIME:
                                    path_progress[k] += 1
                                    last_reach_time[k] = time.time()
                                # If this drone has no remaining section, hold position
                        else:
                            hover_target = np.array([swarm[k].position[0], swarm[k].position[1], FLY_HEIGHT])
                            rpm = swarm[k].step_toward(hover_target)
                            actions[k, :] = rpm

                # --- Check if all helper drones have voted ---
                if len(votes) >= len(verification_targets):
                    print("[Subject] Voting complete!")
                    controller.middle_text = "✅ Subject confirmed! All drones returning home."
                    controller.voting_text += "✅ Subject confirmed — returning home.\n"

                    # Log info
                    total_time = round(time.time() - start_time, 1)
                    controller.middle_text += f"\nSubject confirmed at {np.round(subject_pos[:2], 2)} | Time: {total_time}s"

                    # Trigger return phase
                    returning_home = True
                    voting_active = False

                # Step simulation and continue to next frame
                env.step(actions)
                time.sleep(1 / CTRL_FREQ)
                continue


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
            push_border = avoidance_from_borders(current_pos, (grid_size, grid_size), 1.5, search_offset,
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
                        # --- VISUAL: color searched section green ---
                        cell_center = area.sections[current_section[i]].position  # use .position, not .pos or .cells
                        env.mark_section_as_searched(cell_center)
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
                f"Agent {msg['ID']}: Pos={tuple(np.round(msg['Pos'],2))}, Time={msg['Timer']}s"
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

        env.step(actions)
        time.sleep(1 / CTRL_FREQ)

        # --- Check if all sections are searched ---
        if all(c.searched for c in area.sections) and not returning_home:
            print("The search area is searched! drones will return home together...")
            returning_home = True
            time.sleep(0.4)  # small pause before returning

        if returning_home:
            distances = []
            for i in range(num_agents):
                if crashed[i]:
                    continue #here we are skipping a crashed drone
                pos = np.array(env._getDroneStateVector(i)[0:3])
                dist = np.linalg.norm(pos[:2] - home_targets[i][:2])
                distances.append(dist)
            

            if len(distances) == 0 or all(d < 0.5 for d in distances):  # ← inside same block now
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

                        # Safety: fill any unassigned drones with hover commands
                    for idx in range(num_agents):
                        if np.all(actions[idx] == 0):
                            state = swarm[idx].update()
                            hover_target = np.array([state[0], state[1], FLY_HEIGHT])
                            rpm = swarm[idx].step_toward(hover_target)
                            actions[idx, :] = rpm
                    env.step(actions)
                    time.sleep(1 / CTRL_FREQ)

                # Final landing and power-off
                for i, drone in enumerate(swarm):
                    if crashed[i]:
                        continue
                    state = drone.update()
                    current_pos = np.array(state[0:3])
                    if current_pos[2] > 0.05:
                        # Force final descent
                        p.resetBasePositionAndOrientation(
                            env.DRONE_IDS[i],
                            [home_targets[i][0], home_targets[i][1], 0.05],
                            [0, 0, 0, 1],
                            physicsClientId=env.CLIENT
                        )
                    # Stop all motion
                    p.resetBaseVelocity(env.DRONE_IDS[i], [0, 0, 0], [0, 0, 0], physicsClientId=env.CLIENT)

                print("All drones landed and motors shut down.")
                controller.search_active = False
                controller.simulation_running = False

                break




if __name__ == "__main__":
    main()
