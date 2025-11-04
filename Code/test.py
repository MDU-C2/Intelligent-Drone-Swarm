import time
import numpy as np
import pybullet as p
import controller
from gym_pybullet_drones.FLA402.env import SearchAreaAviary
from gym_pybullet_drones.FLA402.searchArea import SearchArea
from gym_pybullet_drones.FLA402.swarm import generate_drone_positions
from gym_pybullet_drones.FLA402.drone import Drone
from gym_pybullet_drones.FLA402.avoidance import avoidance_from_drones
from gym_pybullet_drones.FLA402.avoidance import avoidance_from_borders
from gym_pybullet_drones.FLA402.avoidance import get_all_positions
from gym_pybullet_drones.FLA402.retasking import RetaskingSystem
from gym_pybullet_drones.FLA402.tables import get_all_health_codes, get_health_name

#NUM_D
# RONES = 4
HOME_POSITION = (0, 0)
FLY_HEIGHT = 1.0
CELL_SWEEP_STEPS = 4
SEARCH_OFFSET = (6, 4)

WAYPOINT_TOLERANCE = 0.10
HOVER_TIME = 0.2
MAX_SPEED = 6.0
CTRL_FREQ = 60
BROADCAST_PERIOD = 5.0  # seconds

def generate_lawnmower_points(center, cell_size, steps):
    """Generate lawn-mower pattern fully inside each cell."""
    cx, cy = center
    half = cell_size / 2
    margin = 0.30 * cell_size   # keep 20% margin
    x1, x2 = cx - half + margin, cx + half - margin
    y1, y2 = cy - half + margin, cy + half - margin
    ys = np.linspace(y1, y2, steps)
    pts = []
    flip = False
    for y in ys:
        if not flip:
            pts += [(x1, y, FLY_HEIGHT), (x2, y, FLY_HEIGHT)]
        else:
            pts += [(x2, y, FLY_HEIGHT), (x1, y, FLY_HEIGHT)]
        flip = not flip
    return pts

def find_nearest_drone(failed_idx, swarm):
    """Return the index of the closest active drone."""
    failed_pos = np.array(swarm[failed_idx].position)
    min_dist, nearest = float("inf"), None
    for j, other in enumerate(swarm):
        if j == failed_idx:
            continue
        pos = np.array(other.position)
        dist = np.linalg.norm(failed_pos[:2] - pos[:2])
        if dist < min_dist:
            min_dist, nearest = dist, j
    return nearest

def clamp_xy_to_area(x, y, grid_size=(3,3), cell_size=1.5, offset=(6,4), margin=0.25):
    rows, cols = grid_size
    half_x = cols * cell_size / 2.0
    half_y = rows * cell_size / 2.0
    cx, cy = offset
    min_x = cx - half_x + margin
    max_x = cx + half_x - margin
    min_y = cy - half_y + margin
    max_y = cy + half_y - margin
    return np.clip(x, min_x, max_x), np.clip(y, min_y, max_y)


def main(num_drones = 4):
    print("Initializing environment...")
    initial_xyzs = generate_drone_positions(num_drones, 0.6, HOME_POSITION)
    env = SearchAreaAviary(
        num_drones=num_drones,
        initial_xyzs=initial_xyzs,
        gui=True,
        grid_size=(3, 3),
        cell_size=1.5,
        home_position=(0, 0),
        search_area_offset=(6, 4)
    )

    area = SearchArea(grid_size=(3, 3), cell_size=1.5, home=SEARCH_OFFSET)
    area.assign_drones(num_drones)
    swarm = [Drone(i, env, initial_xyzs[i]) for i in range(num_drones)]

    drone_tasks = {}
    for drone_id in range(num_drones):
        my_cells = area.get_unsearched_cells(drone_id)
        paths = []
        for cell in my_cells:
            path = generate_lawnmower_points(cell.position, area.cell_size, CELL_SWEEP_STEPS)
            paths.append((cell.id, path))
        drone_tasks[drone_id] = iter(paths)

    print("Mission started. Drones searching assigned cells...")
    current_targets = [None] * num_drones
    path_progress = [0] * num_drones
    last_reach_time = [0] * num_drones
    current_cell = [None] * num_drones
    start_time = time.time()
    last_broadcast = [0.0] * num_drones

    returning_home = False
    home_targets = generate_drone_positions(num_drones, 0.6, HOME_POSITION)
    crashed = [False] * num_drones
    crash_timer = [0.0] * num_drones

    health_dict = get_all_health_codes()
    retasker = RetaskingSystem(home_targets)
    # Example: a per-drone health list (all OK initially)
    health_status = [0] * num_drones  # 0 = OK

    if not hasattr(controller, "injected_fault"):
        controller.injected_fault = None

    while True:
        t = time.time() - start_time
        actions = np.zeros((num_drones, 4))
        # --- Get current positions of all drones for avoidance calculations ---
        all_positions = get_all_positions(env, num_drones)

        # --- Check for injected fault from GUI ---
        if controller.injected_fault:
            fault_drone, fault_code = controller.injected_fault
            health_status[fault_drone] = fault_code
            controller.injected_fault = None  # reset
            fault_name = get_health_name(fault_code)
            print(f"[GUI Inject] Drone {fault_drone} fault set to {fault_name}")


         # --- GUI control ---
        if controller.mission_aborted:
            returning_home = True
            controller.mission_aborted = False
            print("GUI: Mission abort detected, returning home!")

        # Wait until user presses Start Search
        if not controller.search_active and not returning_home:
            time.sleep(0.1)
            continue

        for i, drone in enumerate(swarm):
            state = drone.update()
            current_pos = np.array(state[0:3])
            
            # --- Retasking / fault handling ---
            if health_status[i] != 0:  # non-OK health
                result = retasker.handle(i, health_status[i])
                if result:
                    action = result["action"]

                    if action in ("RETURN_HOME", "PREPARE_RETURN"):
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
                        continue  # skip normal search

                    elif action == "LAND_NOW":
                        # emergency land at current spot
                        target_pos = np.array([current_pos[0], current_pos[1], 0.05])
                        next_pos = current_pos + 0.2 * (target_pos - current_pos)
                        rpm = drone.step_toward(next_pos)
                        actions[i, :] = rpm

                        # --- Reassign this drone's sections to a nearby drone ---
                        neighbor = find_nearest_drone(i, swarm)
                        if neighbor is not None:
                            area.reassign_cells_from_drone(i, neighbor)
                            controller.middle_text = f"Drone {i} emergency landed. Sections reassigned to Drone {neighbor}."
                        else:
                            print(f"No available neighbor to take Drone {i}'s sections.")

                        continue  # skip normal search for this drone
                        
                    elif action in ("HOVER", "REDUCED_ROLE", "HOVER_AND_RECONNECT"):
                        # just hover in place
                        rpm = drone.step_toward(current_pos)
                        actions[i, :] = rpm
                        continue

            # --- Detect crash (persistent) ---
            if not crashed[i]:
                if current_pos[2] <= 0.1:  # near ground
                    if crash_timer[i] == 0.0:
                        crash_timer[i] = time.time()
                    elif time.time() - crash_timer[i] > 6.0:  # stayed low for >1s
                        crashed[i] = True
                        print(f"Drone {i} has crashed! Altitude={current_pos[2]:.2f}")
                        p.addUserDebugText(
                            "CRASHED",
                            [current_pos[0], current_pos[1], 0.1],
                            textColorRGB=[1, 0, 0],
                            textSize=2,
                            lifeTime=0,
                            physicsClientId=env.CLIENT
                        )
                        continue  # skip all control for this drone
                else:
                    crash_timer[i] = 0.0
            else:
                continue  # permanently skip control once marked crashed

           # Broadcast every 5 seconds
            if t - last_broadcast[i] >= BROADCAST_PERIOD:
                msg = drone.broadcast()  # uses Drone.broadcast()
                print(f"[Broadcast] Drone {msg['ID']} at {msg['Pos']} | Time: {msg['Timer']}s")
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
                    continue
                current_targets[i] = path
                path_progress[i] = 0
                current_cell[i] = cell_id
                last_reach_time[i] = time.time()  # prevent initial hover pause
                print(f"Drone {i} → new cell {cell_id}")

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
            
            rpm = drone.step_toward(next_pos)
            actions[i, :] = rpm

            if dist < WAYPOINT_TOLERANCE:
                if time.time() - last_reach_time[i] > HOVER_TIME:
                    path_progress[i] += 1
                    last_reach_time[i] = time.time()
                    if path_progress[i] >= len(current_targets[i]):
                        area.mark_searched(current_cell[i])
                        print(f"Drone {i} finished cell {current_cell[i]}")
                        current_targets[i] = None

        # --- Update GUI displays via controller ---
        broadcast_lines = []
        for i, drone in enumerate(swarm):
            msg = drone.broadcast()
            broadcast_lines.append(
                f"Drone {msg['ID']}: Pos={tuple(np.round(msg['Pos'],2))}, Time={msg['Timer']}s"
            )
        controller.broadcast_text = "\n".join(broadcast_lines)

        assign_lines = []
        for i in range(num_drones):
            cells = [c.id for c in area.cells if c.assigned_drone == i]
            assign_lines.append(f"Drone {i}: Cells {cells}")
        controller.assignment_text = "\n".join(assign_lines)

        env.step(actions)
        time.sleep(1 / CTRL_FREQ)

        # --- Check if all cells are searched ---
        if all(c.searched for c in area.cells) and not returning_home:
            print("All cells searched! Drones will return home together...")
            returning_home = True
            time.sleep(1.5)  # small pause before returning

        if returning_home:
            distances = []
            for i in range(num_drones):
                if crashed[i]:
                    continue #here we are skipping a crashed drone
                pos = np.array(env._getDroneStateVector(i)[0:3])
                dist = np.linalg.norm(pos[:2] - home_targets[i][:2])
                distances.append(dist)
            

            if len(distances) == 0 or all(d < 0.2 for d in distances):  # ← inside same block now
                print("All drones returned home. Mission complete!")
                 # Gradually descend to z=0

                for _ in range(int(CTRL_FREQ * 40)):  # ~15 seconds descent
                    actions = np.zeros((num_drones, 4))
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
