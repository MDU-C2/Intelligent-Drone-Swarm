# populate_test_data.py

from database.core.paths import DB_NAME_TXT
from ..core.connect_database import connect_database
from ..core.create_tables import create_tables
from ..core.insert_functions import insert_functions

db_name = DB_NAME_TXT.read_text().strip()

with connect_database(db_name) as db:
    tables = create_tables(db.cursor)
    tables.create_all_tables()

    inserter = insert_functions(db.cursor, db.conn)

    # ----- Documents -----
    # doc_id, title, description, file, version, author ('E.Z','C.N','Y.M.B','E.M','A.H')
    d1 = inserter.insert_documents(None, "Swarm Test Spec", "Swarm subsystem tests", None, 1, "A.H")
    d2 = inserter.insert_documents(None, "System V&V Plan", "System-level test plan", None, 1, "C.N")
    d3 = inserter.insert_documents(None, "Subsystem Spec", "Subsystem test spec", None, 1, "E.Z")
    d4 = inserter.insert_documents(None, "Quality Plan", "QA plan for all levels", None, 2, "Y.M.B")

    # ----- Test & Verification Methods -----
    # method_id, description, method_type ('Inspection','Analysis','Test')
    m1 = inserter.insert_test_and_verification(None, "Visual Inspection", "Inspection")
    m2 = inserter.insert_test_and_verification(None, "Functional Test", "Test")
    m3 = inserter.insert_test_and_verification(None, "Simulation Analysis", "Analysis")
    m4 = inserter.insert_test_and_verification(None, "Full Flight Test", "Test")

    # ----- Link Methods to Docs -----
    # id, method_id, doc_id
    inserter.insert_V_join_documents(m1, d1)
    inserter.insert_V_join_documents(m2, d2)
    inserter.insert_V_join_documents(m3, d3)
    inserter.insert_V_join_documents(m4, d4)

    # ----- Goals -----
    # goal_id, goal_description, stakeholder, origin, priority ('Key','Mandatory','Optional'),
    # rationale, satisfaction_status ('Pending','Not satisfied','Satisfied'), method_id
    g1 = inserter.insert_goal(None, "Ensure swarm formation control", "C.N", "Spec v1", "Key", "Core feature", "Pending", None)
    g2 = inserter.insert_goal(None, "Maintain comms integrity", "Y.M.B", "Spec v2", "Mandatory", "Essential for safety", "Not satisfied", "M-02")
    g3 = inserter.insert_goal(None, "Reduce power consumption", "A.H", "Design v3", "Optional", "Optimization goal", "Satisfied", "M-03")

    # ----- Drone Swarm Requirements -----
    # swarm_req_id, requirement, priority ('Key','Mandatory','Optional'), effect, rationale,
    # author ('E.Z','C.N','Y.M.B','E.M','A.H'), verification_status ('TBR','Reviewed','Accepted', 'Rejected')
    # verifier ('E.Z','C.N','Y.M.B','E.M','A.H','TBR'), 
    # validation_status ('Pending','Failed','Verified','Inconclusive'), vv_method,
    # comment
    sw1 = inserter.insert_drone_swarm_requirements(
        None, "Maintain formation at 5m spacing", "Key", "Formation stability", "Core mission behavior",
        "C.N", "TBR", "A.H", "Verified", "M-01", "Basic test done."
    )
    sw2 = inserter.insert_drone_swarm_requirements(
        None, "Auto-adjust comms channels", "Mandatory", "Reliable swarm control", "Avoid interference",
        "E.Z", "Reviewed", "Y.M.B", "Failed", "M-02", "Issue detected in simulation."
    )
    sw3 = inserter.insert_drone_swarm_requirements(
        None, "Battery health reporting", "Optional", "Power management", "Improves maintenance",
        "E.M", "Accepted", "A.H", "Verified", "M-03"
    )

    # ----- System Requirements -----
    # parent_id, sys_req_id, requirement, priority ('Key','Mandatory','Optional'), effect, rationale, 
    # author ('E.Z','C.N','Y.M.B','E.M','A.H'), verification_status ('TBR','Reviewed','Accepted', 'Rejected')
    # verifier ('E.Z','C.N','Y.M.B','E.M','A.H','TBR'), 
    # validation_status ('Pending','Failed','Verified','Inconclusive'), vv_method,
    # comment
    sys1 = inserter.insert_system_requirements(
        None, None, "Control CPU handles swarm formation", "Key", "Control logic",
        "Initial version", "Y.M.B", "Reviewed", "E.Z", "Verified", "M-01"
    )
    sys2 = inserter.insert_system_requirements(
        sys1, None, "Add fault-tolerant communication module", "Mandatory", "Comms redundancy",
        "Ensures resilience", "E.Z", "Reviewed", "C.N", "Pending"
    )
    sys3 = inserter.insert_system_requirements(
        None, None, "Optimize CPU load distribution", "Optional", "Efficiency improvement",
        "Performance goal", "C.N", "Accepted", "Y.M.B", "Verified", "M-03"
    )
    sys4 = inserter.insert_system_requirements(
        None, None, "Implement OTA update feature", "Mandatory", "Maintainability",
        "System flexibility", "A.H", "TBR", "E.Z", "Failed", "M-04"
    )

    # ----- Subsystem Requirements -----
    # parent_id, sub_req_id, requirement, priority ('Key','Mandatory','Optional'), effect, rationale, 
    # author ('E.Z','C.N','Y.M.B','E.M','A.H'), verification_status ('TBR','Reviewed','Accepted', 'Rejected')
    # verifier ('E.Z','C.N','Y.M.B','E.M','A.H','TBR'), 
    # validation_status ('Pending','Failed','Verified','Inconclusive'), vv_method,
    # comment
    ss1 = inserter.insert_subsystem_requirements(
        None, None, "Design motor control firmware", "Key", "Flight performance",
        "Initial design", "C.N", "Reviewed", "A.H", "Verified", "M-02"
    )
    ss2 = inserter.insert_subsystem_requirements(
        None, None, "Integrate redundant power buses", "Mandatory", "Power stability",
        "Avoid single-point failures", "Y.M.B", "TBR", "E.Z", "Pending"
    )
    ss3 = inserter.insert_subsystem_requirements(
        ss1, None, "Add thermal protection layer", "Optional", "Component safety",
        "High-temp areas", "E.Z", "Accepted", "C.N", "Verified", "M-03"
    )
    ss4 = inserter.insert_subsystem_requirements(
        None, None, "Implement subsystem diagnostics", "Key", "Health monitoring",
        "Critical for maintenance", "E.M", "Accepted", "Y.M.B", "Verified", "M-04"
    )
    ss5 = inserter.insert_subsystem_requirements(
        ss4, None, "Add signal filtering for sensors", "Mandatory", "Noise reduction",
        "Ensures stable readings", "E.Z", "Reviewed", "C.N", "Pending"
    )

    # ----- Items -----
    # item_id, item_name
    i1 = inserter.insert_item(None, "Motor Controller Board")
    i2 = inserter.insert_item(None, "Communication Module")
    i3 = inserter.insert_item(None, "Battery Pack")

    # ----- Joins -----
    inserter.insert_goal_children(g1, sw1)
    inserter.insert_goal_children(g2, sw2)
    inserter.insert_goal_children(g3, sw3)

    inserter.insert_swarm_req_children(sw1, sys1)
    inserter.insert_swarm_req_children(sw2, sys3)
    inserter.insert_swarm_req_children(sw3, sys4)

    inserter.insert_sysreq_children(sys1, ss1)
    inserter.insert_sysreq_children(sys2, ss3)
    inserter.insert_sysreq_children(sys3, ss4)

    inserter.insert_subsys_join_item(i1, ss1)
    inserter.insert_subsys_join_item(i2, ss4)
    inserter.insert_subsys_join_item(i3, ss5)

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
    inserter.insert_quality_requirements(None, "All communication shall be encrypted", "E.Z", "Y.M.B")
    inserter.insert_quality_requirements(None, "System shall meet 95% uptime", "C.N", "Y.M.B")

print("Database populated with extended demo data!")
