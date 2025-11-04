import random
from gym_pybullet_drones.FLA402.tables import HEALTH_TABLE

def inject_fault_to_drone(drone, fault: str):
    """
    Set a specific health fault on a Drone object.
    drone: instance of Drone (drone.set_health exists).
    fault: key from HEALTH_TABLE, e.g. "BAD_BATTERY"
    """
    if fault not in HEALTH_TABLE:
        raise ValueError(f"Unknown fault '{fault}'")
    print(f"[FaultInj] Injecting '{fault}' into drone {drone.id}")
    drone.set_health(fault)

def inject_random_fault(swarm, fault="BAD_BATTERY"):
    """
    Pick a random drone from swarm (list of Drone objects) and mark it faulty.
    """
    if len(swarm) == 0:
        return None
    d = random.choice(swarm)
    inject_fault_to_drone(d, fault)
    return d
