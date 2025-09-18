import unittest
import os
from Database_code.db_functions import req_database  

class TestReqDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_database.db"
        # Ensure clean slate
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def table_exists(self, cursor, table_name):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return cursor.fetchone() is not None

    def test_create_all_tables(self):
        with req_database(self.test_db) as db:
            db.create_all_tables()
            # Check whether each table exists
            for table in [
                "goals",
                "system_requirements",
                "goal_children",
                "subsystem_requirements",
                "sysreq_children",
                "sys_join_item",
                "item",
                "documents",
                "test_and_verification",
                "V_join_documents"
                
            ]:
                 exists = self.table_exists(db.cursor, table)
                 print(f"Checking table: {table} → Exists: {exists}")
                 self.assertTrue(exists, f"Missing table: {table}")

if __name__ == "__main__":
    unittest.main()