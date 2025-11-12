import threading
import main
import pybullet as p

# Control flags
simulation_running = False
search_active = False
mission_aborted = False

# Shared text for GUI
broadcast_text = ""
assignment_text = ""
voting_text = ""             
# Fault injection & health feedback
injected_fault = None      # (drone_id, health_code)
middle_text = ""           # Text from test.py for GUI display
home_ready = []            # list of booleans, same length as number of drones
charged_drones = set()     # track drones that have been charged




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
    print("Mission aborted! Returning agents to base.")

def mark_drone_charged(drone_id):
    """Called from GUI when the Charge button is pressed."""
    global home_ready, charged_drones
    if len(home_ready) > drone_id and home_ready[drone_id]:
        charged_drones.add(drone_id)
        home_ready[drone_id] = False  # reset flag
        print(f"[Controller] Drone {drone_id} marked as charged.")

def run_simulation(num_drones=4, grid_size=4):
    global simulation_running, search_active, mission_aborted, _sim_thread
    global home_ready, charged_drones
    home_ready = [False] * num_drones
    charged_drones = set()

    if simulation_running:
        print("Simulation already running.")
        return

    simulation_running = True
    search_active = False
    mission_aborted = False

    print(f"Launching simulation with {num_drones} drones on {grid_size}x{grid_size} grid...")

    def _run():
        try:
            main.main(num_drones, grid_size)
        except SystemExit:
            pass
        except Exception as e:
            print(f"[Controller] Simulation thread exception: {e}")
        finally:
            if p.isConnected():
                p.disconnect()
            print("[Controller] Simulation thread finished.")
            simulation_running = False

    _sim_thread = threading.Thread(target=_run, daemon=True)
    _sim_thread.start()