import threading
import test

# Control flags
simulation_running = False
search_active = False
mission_aborted = False

# Shared text for GUI
broadcast_text = ""
assignment_text = ""
# Fault injection & health feedback
injected_fault = None      # (drone_id, health_code)
middle_text = ""           # Text from test.py for GUI display



def start_search():
    global search_active, mission_aborted
    if not simulation_running:
        print("Simulation not started yet!")
        return
    mission_aborted = False
    search_active = True
    print("Search started!")


def abort_mission():
    global search_active, mission_aborted
    if not simulation_running:
        print("Simulation not running!")
        return
    search_active = False
    mission_aborted = True
    print("Mission aborted! Returning drones to base.")


def run_simulation(num_drones=4):
    global simulation_running, search_active, mission_aborted
    if simulation_running:
        print("Simulation already running.")
        return
    simulation_running = True
    search_active = False
    mission_aborted = False

    print(f"Launching simulation with {num_drones} drones...")
    thread = threading.Thread(target=test.main, args=(num_drones,))
    thread.start()
