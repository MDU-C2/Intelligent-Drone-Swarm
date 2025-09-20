import unittest

from database-code.db_functions import req_database

class TestInsertAllTables(unittest.TestCase):
    def setUp(self):
        self.db = req_database(":memory:")
        self.db.__enter__()

        # Create all tables
        self.db.create_all_tables()
        

        # Insert shared references
        self.db.insert_test_and_verification('M1', 'Visual inspection', 'Inspection')
        self.db.insert_documents('D1', 'Protocol', 'Swarm rules', None, 1, 'E.Z')
        self.db.insert_item('I1', 'Drone Sensor')

    def tearDown(self):
        self.db.__exit__(None, None, None)

    def test_insert_all(self):


        # Goal
        self.db.insert_goal ('G1', 'Avoid collisions', 'Operator', 'Brief', 'Key', 'Safety', 'Pending', 'M1')
        self.db.insert_drone_swarm_requirements("DS1", "Maintain formation", "Key", "Improved stability", "Essential for coordination",
             "E.Z", "Reviewed", "C.N", "Verified", "M1", "No issues")

        # System Requirement
        self.db.insert_system_requirements(None, 'SR1', 'Reliable comms', 'Mandatory', 'Robustness', 'Essential',
                'E.Z', 'Reviewed', 'C.N', 'Pass', 'M1', 'Tested')
        

        # Subsystem Requirement
        self.db.insert_subsystem_requirements(None, 'SUB1', 'Encrypt data', 'Key', 'Security', 'Vital',
                'E.Z', 'Reviewed', 'C.N', 'Verified', 'M1', 'Encrypted')
    

        # Goal Children
        self.db.insert_goal_children('G1', 'DS1')

        # Swarm Req Children
        self.db.insert_swarm_req_children('DS1', 'SR1')

        # SysReq Children
        self.db.insert_sysreq_children('SR1', 'SUB1')

        # Sys Join Item
        self.db.insert_sys_join_item('I1', 'SUB1')


        # Verification Join Document
        self.db.insert_V_join_documents('M1', 'D1')

        # Final check
        self.db.cursor.execute("SELECT COUNT(*) FROM goals")
        self.assertEqual(self.db.cursor.fetchone()[0], 1)

        self.db.cursor.execute("SELECT COUNT(*) FROM system_requirements")
        self.assertEqual(self.db.cursor.fetchone()[0], 1)

        self.db.cursor.execute("SELECT COUNT(*) FROM subsystem_requirements")
        self.assertEqual(self.db.cursor.fetchone()[0], 1)

        self.db.cursor.execute("SELECT COUNT(*) FROM drone_swarm_requirements")
        self.assertEqual(self.db.cursor.fetchone()[0], 1)

    
        self.db.cursor.execute("SELECT COUNT(*) FROM sys_join_item")
        self.assertEqual(self.db.cursor.fetchone()[0], 1)

        self.db.cursor.execute("SELECT COUNT(*) FROM V_join_documents")
        self.assertEqual(self.db.cursor.fetchone()[0], 1)

if __name__ == "__main__":
    unittest.main()
