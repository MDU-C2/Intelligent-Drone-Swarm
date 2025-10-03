# test.py

from connect_database import connect_database
from create_tables import create_tables
from insert_functions import insert_functions

with open("db_name.txt") as f:
    db_name = f.read().strip() 

with connect_database(db_name) as db:
    # Ensure all tables exist
    tables = create_tables(db.cursor)
    tables.create_all_tables()

    # Create an inserter
    inserter = insert_functions(db.cursor)

    # --- Insert Documents ---
    inserter.insert_documents("D-01", "Doc Title", "Swarm test", None, None, "A.H")
    inserter.insert_documents("D-02", "Doc Title", "Sys test", None, None, "C.N")
    inserter.insert_documents("D-03", "Doc Title", "Subsys test", None, None, "A.H")

    # Insert Test & Verification
    inserter.insert_test_and_verification("M-01", "Method 1", "Inspection")
    inserter.insert_test_and_verification("M-02", "Method 2", "Inspection")
    inserter.insert_test_and_verification("M-03", "Method 3", "Inspection")

    # Insert V join docs
    inserter.insert_V_join_documents("M-01", "D-01")
    inserter.insert_V_join_documents("M-02", "D-02")
    inserter.insert_V_join_documents("M-02", "D-03")

    # --- Insert Goals ---
    inserter.insert_goal("G-01", "The aim is to test our first constraint implementation", "requirements manager", None, "Key", None, "Not satisfied", None)

    # --- Insert Drone Swarm Requirements ---
    inserter.insert_drone_swarm_requirements(
        "SW-01", "First swarm requirement", "Key", "Effect", None,
        "C.N", "TBR", "A.H", "Verified", "M-01")
    inserter.insert_drone_swarm_requirements(
        "SW-02", "Test 1 constraint", "Key", "Results", None,
        "C.N", "TBR", "A.H", "Verified", "M-01"
    )

    # --- Insert System Requirements ---
    inserter.insert_system_requirements(
        None, "CP-03", "TEST3 next constraint", "Key", "function db",
        None, "C.N", "TBR", "E.Z", "Failed", "M-02"
    )
    inserter.insert_system_requirements(
        None, "CP-04", "TEST3 next constraint", "Key", "function db",
        None, "C.N", "TBR", "E.Z", "Pending"
    )
    inserter.insert_system_requirements(
        "CP-03", "CP-05", "TEST 3 next constraint", "Key", "function db",
        None, "C.N", "TBR", "A.H", "Pending"
    )

    # --- Insert Subsystem Requirements ---
    inserter.insert_subsystem_requirements(
        None, "B-01", "Test sub sys req", "Key", "function_children",
        None, "C.N", "TBR", "E.Z", "Failed", "M-03"
    )
    inserter.insert_subsystem_requirements(
        None, "B-02", "Test sub sys req", "Key", "function_children",
        None, "C.N", "TBR", "E.Z", "Pending"
    )
    inserter.insert_subsystem_requirements(

        None, "B-03", "Test sub sys req", "Key", "function_children",
        None, "C.N", "TBR", "E.Z", "Pending"
    )
    inserter.insert_subsystem_requirements(
        
        "B-03", "B-05", "Test sub sys req", "Key", "function_children",
        None, "C.N", "TBR", "E.Z", "Pending"
    )

    # --- Insert Goal-Child Relationships ---
    inserter.insert_goal_children("G-01", "SW-01")
    inserter.insert_goal_children("G-01", "SW-02")

    # --- Insert Swarm Req → System Req Relationships ---
    inserter.insert_swarm_req_children("SW-01", "CP-03")
    inserter.insert_swarm_req_children("SW-02", "CP-04")

    # --- Insert System Req → Subsystem Req Relationships ---
    inserter.insert_sysreq_children("CP-03", "B-01")
    inserter.insert_sysreq_children("CP-04", "B-02")
    inserter.insert_sysreq_children("CP-03", "B-03")