
import unittest
from database_code.db_functions import req_database  # adjust import if needed

class TestDatabaseInsertions(unittest.TestCase):
    def setUp(self):
        # Use in-memory database for testing
        self.db_name = ":memory:"
        self.db = req_database(self.db_name)
        self.db.__enter__()

        # Create necessary tables
        self.db.create_test_and_verification_table()
        self.db.create_goals_table()
        self.db.create_drone_swarm_requirements_table()
        self.db.create_documents_table()

    def tearDown(self):
        self.db.__exit__(None, None, None)

    def test_insert_into_test_and_verification(self):
        self.db.cursor.execute(
            "INSERT INTO test_and_verification (method_id, description, method_type) VALUES (?, ?, ?)",
            ("M1", "Visual inspection of drone", "Inspection")
        )
        self.db.cursor.execute("SELECT * FROM test_and_verification WHERE method_id = ?", ("M1",))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "M1")

    def test_insert_into_goals(self):
        # Insert prerequisite method
        self.db.cursor.execute(
            "INSERT INTO test_and_verification (method_id, description, method_type) VALUES (?, ?, ?)",
            ("M2", "Analysis of flight path", "Analysis")
        )
        self.db.cursor.execute(
            """
            INSERT INTO goals (goal_id, goal_description, stakeholder, origin, priority, rationale, satisfaction_status, method_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("G1", "Ensure safe navigation", "Operator", "Mission Brief", "Mandatory", "Safety critical", "Pending", "M2")
        )
        self.db.cursor.execute("SELECT * FROM goals WHERE goal_id = ?", ("G1",))
        result = self.db.cursor.fetchone()
        self.assertEqual(result[0], "G1")

    def test_insert_into_drone_swarm_requirements(self):
        # Insert prerequisite method
        self.db.cursor.execute(
            "INSERT INTO test_and_verification (method_id, description, method_type) VALUES (?, ?, ?)",
            ("M3", "Test swarm coordination", "Test")
        )
        self.db.cursor.execute(
            """
            INSERT INTO drone_swarm_requirements (
                swarm_req_id, requirement, priority, effect, rationale,
                author, review_status, reviewer, verification_status,
                verification_method, comment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("DS1", "Maintain formation", "Key", "Improved stability", "Essential for coordination",
             "E.Z", "Reviewed", "C.N", "Verified", "M3", "No issues")
        )
        self.db.cursor.execute("SELECT * FROM drone_swarm_requirements WHERE swarm_req_id = ?", ("DS1",))
        result = self.db.cursor.fetchone()
        self.assertEqual(result[0], "DS1")

    def test_insert_into_documents(self):
        self.db.cursor.execute(
            """
            INSERT INTO documents (doc_id, title, description, file, version, author)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("D1", "Swarm Protocol", "Defines communication rules", None, 1, "Y.M.B")
        )
        self.db.cursor.execute("SELECT * FROM documents WHERE doc_id = ?", ("D1",))
        result = self.db.cursor.fetchone()
        self.assertEqual(result[0], "D1")

if __name__ == "__main__":
    unittest.main()
