import numpy as np
import pybullet as p
import time
import threading
from gym_pybullet_drones.FLA402.env import SearchAreaAviary 
from gym_pybullet_drones.FLA402.drones import generate_drone_positions
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.enums import DroneModel

# -------------------------------
# Global flags for GUI interaction
# -------------------------------
search_active = False
simulation_running = False
mission_aborted = False

def start_search():
    global search_active, mission_aborted
    mission_aborted = False
    search_active = True
    print("Search started!")

def abort_mission():
    global search_active, mission_aborted
    search_active = False
    mission_aborted = True
    print("ABORT MISSION! Drones returning to home formation...")

def run_simulation(num_drones=9):
    """Main simulation function."""
    global simulation_running, search_active, mission_aborted
    if simulation_running:
        print("Simulation already running.")
        return
    simulation_running = True
    search_active = False
    mission_aborted = False

    # --- Configuration ---
    NUM_DRONES = num_drones
    FORMATION_RADIUS = 0.4
    HOME_POSITION = (0, 0)
    FLY_HEIGHT = 1.0
    RANDOM_TURN_INTERVAL = 3.0
    SEARCH_TIME = 5.0  # seconds per grid cell

    # --- Setup environment ---
    initial_xyzs = generate_drone_positions(NUM_DRONES, FORMATION_RADIUS, HOME_POSITION)
    env = SearchAreaAviary(
        num_drones=NUM_DRONES,
        initial_xyzs=initial_xyzs,
        gui=True,
        record=False,
        grid_size=(10, 10),
        cell_size=1.0,
        home_position=HOME_POSITION
    )

    print(f"{NUM_DRONES} drones initialized. Waiting for 'Start Search'...")

    p.setGravity(0, 0, -env.G, physicsClientId=env.CLIENT)

    ctrl = [DSLPIDControl(drone_model=DroneModel.CF2X) for _ in range(NUM_DRONES)]

    # Setup grid targets. This will be changed later, it's just to simulate how they would be to the grid and 'search'.   
    grid_positions = []
    for i in range(3):
        for j in range(3):
            x = (i - 1) * 1.5
            y = (j - 1) * 1.5
            grid_positions.append((x, y))
    drone_targets = grid_positions[:NUM_DRONES]
    drone_done = [False] * NUM_DRONES
    search_start = [None] * NUM_DRONES
    home_positions = np.copy(initial_xyzs)

    last_change = time.time()

    while True:
        if not search_active and not mission_aborted:
            time.sleep(0.1)
            continue

        actions = np.zeros((NUM_DRONES, 4))
        for i in range(NUM_DRONES):
            state = env._getDroneStateVector(i)
            pos = np.array(state[0:3])

            if mission_aborted:
                home_target = np.array([home_positions[i][0], home_positions[i][1], FLY_HEIGHT])
                target_pos = pos + 0.2 * (home_target - pos)
            else:
                target_xy = np.array([drone_targets[i][0], drone_targets[i][1], FLY_HEIGHT])
                target_pos = pos + 0.05 * (target_xy - pos)

            rpm, _, _ = ctrl[i].computeControlFromState(
                control_timestep=1/env.CTRL_FREQ,
                state=state,
                target_pos=target_pos
            )
            actions[i, :] = rpm

            if not mission_aborted:
                dist = np.linalg.norm(np.array([drone_targets[i][0], drone_targets[i][1]]) - pos[:2])
                if dist < 0.3 and not drone_done[i]:
                    if search_start[i] is None:
                        search_start[i] = time.time()
                        print(f"Drone {i} started searching cell.")
                    elif time.time() - search_start[i] > SEARCH_TIME:
                        drone_done[i] = True
                        print(f"Drone {i} finished searching its cell.")

        env.step(actions)
        time.sleep(1 / env.CTRL_FREQ)

        if all(drone_done) and not mission_aborted:
            print("All drones finished searching.")
            search_active = False

        if mission_aborted:
            all_home = True
            for i in range(NUM_DRONES):
                pos = np.array(env._getDroneStateVector(i)[0:3])
                dist_to_home = np.linalg.norm(pos[:2] - home_positions[i][:2])
                if dist_to_home > 0.3:
                    all_home = False
                    break
            if all_home:
                print("All drones have returned to their home formation safely.")
                mission_aborted = False
                search_active = False

if __name__ == "__main__":
    t = threading.Thread(target=run_simulation, args=(9,))
    t.start()
    while not simulation_running:
        time.sleep(0.5)
    input("Press ENTER to start search...\n")
    start_search()
