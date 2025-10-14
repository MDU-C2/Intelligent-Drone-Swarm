# populate_test_data.py

from pathlib import Path
from ..core.connect_database import connect_database
from ..core.create_tables import create_tables
from ..core.insert_functions import insert_functions

DB_NAME_PATH = Path(__file__).resolve().parents[1] / "data" / "db_name.txt"

with open(DB_NAME_PATH) as f:
    db_name = f.read().strip()

with connect_database(db_name) as db:
    tables = create_tables(db.cursor)
    tables.create_all_tables()

    inserter = insert_functions(db.cursor)

    # ----- Documents -----
    # doc_id, title, description, file, version, author ('E.Z','C.N','Y.M.B','E.M','A.H')
    inserter.insert_documents("D-01", "Swarm Test Spec", "Swarm subsystem tests", None, 1, "A.H")
    inserter.insert_documents("D-02", "System V&V Plan", "System-level test plan", None, 1, "C.N")
    inserter.insert_documents("D-03", "Subsystem Spec", "Subsystem test spec", None, 1, "E.Z")
    inserter.insert_documents("D-04", "Quality Plan", "QA plan for all levels", None, 2, "Y.M.B")

    # ----- Test & Verification Methods -----
    # method_id, description, method_type ('Inspection','Analysis','Test')
    inserter.insert_test_and_verification("M-01", "Visual Inspection", "Inspection")
    inserter.insert_test_and_verification("M-02", "Functional Test", "Test")
    inserter.insert_test_and_verification("M-03", "Simulation Analysis", "Analysis")
    inserter.insert_test_and_verification("M-04", "Full Flight Test", "Test")

    # ----- Link Methods to Docs -----
    # id, method_id, doc_id
    inserter.insert_V_join_documents("M-01", "D-01")
    inserter.insert_V_join_documents("M-02", "D-02")
    inserter.insert_V_join_documents("M-03", "D-03")
    inserter.insert_V_join_documents("M-04", "D-04")

    # ----- Goals -----
    # goal_id, goal_description, stakeholder, origin, priority ('Key','Mandatory','Optional'),
    # rationale, satisfaction_status ('Pending','Not satisfied','Satisfied'), method_id
    inserter.insert_goal("G-01", "Ensure swarm formation control", "C.N", "Spec v1", "Key", "Core feature", "Pending", None)
    inserter.insert_goal("G-02", "Maintain comms integrity", "Y.M.B", "Spec v2", "Mandatory", "Essential for safety", "Not satisfied", "M-02")
    inserter.insert_goal("G-03", "Reduce power consumption", "A.H", "Design v3", "Optional", "Optimization goal", "Satisfied", "M-03")

    # ----- Drone Swarm Requirements -----
    # swarm_req_id, requirement, priority ('Key','Mandatory','Optional'), effect, rationale,
    # author ('E.Z','C.N','Y.M.B','E.M','A.H'), review_status ('TBR','Reviewed','Accepted', 'Rejected')
    # reviewer ('E.Z','C.N','Y.M.B','E.M','A.H','TBR'), 
    # verification_status ('Pending','Failed','Verified','Inconclusive'), verification_method,
    # comment
    inserter.insert_drone_swarm_requirements(
        "SW-01", "Maintain formation at 5m spacing", "Key", "Formation stability", "Core mission behavior",
        "C.N", "TBR", "A.H", "Verified", "M-01", "Basic test done."
    )
    inserter.insert_drone_swarm_requirements(
        "SW-02", "Auto-adjust comms channels", "Mandatory", "Reliable swarm control", "Avoid interference",
        "E.Z", "Reviewed", "Y.M.B", "Failed", "M-02", "Issue detected in simulation."
    )
    inserter.insert_drone_swarm_requirements(
        "SW-03", "Battery health reporting", "Optional", "Power management", "Improves maintenance",
        "E.M", "Accepted", "A.H", "Verified", "M-03"
    )

    # ----- System Requirements -----
    # parent_id, sys_req_id, requirement, priority ('Key','Mandatory','Optional'), effect, rationale, 
    # author ('E.Z','C.N','Y.M.B','E.M','A.H'), review_status ('TBR','Reviewed','Accepted', 'Rejected')
    # reviewer ('E.Z','C.N','Y.M.B','E.M','A.H','TBR'), 
    # verification_status ('Pending','Failed','Verified','Inconclusive'), verification_method,
    # comment
    inserter.insert_system_requirements(
        None, "SYS-01", "Control CPU handles swarm formation", "Key", "Control logic",
        "Initial version", "Y.M.B", "Reviewed", "E.Z", "Verified", "M-01"
    )
    inserter.insert_system_requirements(
        "SYS-01", "SYS-02", "Add fault-tolerant communication module", "Mandatory", "Comms redundancy",
        "Ensures resilience", "E.Z", "Reviewed", "C.N", "Pending"
    )
    inserter.insert_system_requirements(
        None, "SYS-03", "Optimize CPU load distribution", "Optional", "Efficiency improvement",
        "Performance goal", "C.N", "Accepted", "Y.M.B", "Verified", "M-03"
    )
    inserter.insert_system_requirements(
        None, "SYS-04", "Implement OTA update feature", "Mandatory", "Maintainability",
        "System flexibility", "A.H", "TBR", "E.Z", "Failed", "M-04"
    )

    # ----- Subsystem Requirements -----
    # parent_id, sub_req_id, requirement, priority ('Key','Mandatory','Optional'), effect, rationale, 
    # author ('E.Z','C.N','Y.M.B','E.M','A.H'), review_status ('TBR','Reviewed','Accepted', 'Rejected')
    # reviewer ('E.Z','C.N','Y.M.B','E.M','A.H','TBR'), 
    # verification_status ('Pending','Failed','Verified','Inconclusive'), verification_method,
    # comment
    inserter.insert_subsystem_requirements(
        None, "SS-01", "Design motor control firmware", "Key", "Flight performance",
        "Initial design", "C.N", "Reviewed", "A.H", "Verified", "M-02"
    )
    inserter.insert_subsystem_requirements(
        None, "SS-02", "Integrate redundant power buses", "Mandatory", "Power stability",
        "Avoid single-point failures", "Y.M.B", "TBR", "E.Z", "Pending"
    )
    inserter.insert_subsystem_requirements(
        "SS-01", "SS-03", "Add thermal protection layer", "Optional", "Component safety",
        "High-temp areas", "E.Z", "Accepted", "C.N", "Verified", "M-03"
    )
    inserter.insert_subsystem_requirements(
        None, "SS-04", "Implement subsystem diagnostics", "Key", "Health monitoring",
        "Critical for maintenance", "E.M", "Accepted", "Y.M.B", "Verified", "M-04"
    )
    inserter.insert_subsystem_requirements(
        "SS-04", "SS-05", "Add signal filtering for sensors", "Mandatory", "Noise reduction",
        "Ensures stable readings", "E.Z", "Reviewed", "C.N", "Pending"
    )

    # ----- Items -----
    # item_id, item_name
    inserter.insert_item("I-01", "Motor Controller Board")
    inserter.insert_item("I-02", "Communication Module")
    inserter.insert_item("I-03", "Battery Pack")

    # ----- Joins -----
    inserter.insert_goal_children("G-01", "SW-01")
    inserter.insert_goal_children("G-02", "SW-02")
    inserter.insert_goal_children("G-03", "SW-03")

    inserter.insert_swarm_req_children("SW-01", "SYS-01")
    inserter.insert_swarm_req_children("SW-02", "SYS-03")
    inserter.insert_swarm_req_children("SW-03", "SYS-04")

    inserter.insert_sysreq_children("SYS-01", "SS-01")
    inserter.insert_sysreq_children("SYS-02", "SS-03")
    inserter.insert_sysreq_children("SYS-03", "SS-04")

    inserter.insert_subsys_join_item("I-01", "SS-01")
    inserter.insert_subsys_join_item("I-02", "SS-04")
    inserter.insert_subsys_join_item("I-03", "SS-05")

    # ----- Glossary -----
    # gloss_id, prefix, meaning
    inserter.insert_id_glossary("G", "Goal")
    inserter.insert_id_glossary("SW", "Swarm Requirement")
    inserter.insert_id_glossary("SYS", "System Requirement")
    inserter.insert_id_glossary("SS", "Subsystem Requirement")
    inserter.insert_id_glossary("I", "Item")
    inserter.insert_id_glossary("M", "V&V Method")
    inserter.insert_id_glossary("D", "Document")

    # ----- Quality Requirements -----
    # qualite_rec_id, requirement, author ('E.Z','C.N','Y.M.B','E.M','A.H'), 
    # approved_by (('Y.M.B') OR NULL))
    inserter.insert_quality_requirements("QR-01", "All communication shall be encrypted", "E.Z", "Y.M.B")
    inserter.insert_quality_requirements("QR-02", "System shall meet 95% uptime", "C.N", "Y.M.B")

print("Database populated with extended demo data!")
