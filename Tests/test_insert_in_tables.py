import unittest
from database_code.db_functions import req_database  # adjust path as needed


class TestReqDatabaseInserts(unittest.TestCase):
    def setUp(self):
        self.test_db = ":memory:"
        self.db = req_database(self.test_db)
        self.db.__enter__()
        self.db.create_all_tables()

    def tearDown(self):
        self.db.__exit__(None, None, None)

    def test_insert_goal(self):
        self.db.insert_goal("G1", "Safety", "Operator", "Spec", "Key", "Critical")
        self.db.cursor.execute("SELECT * FROM goals WHERE goal_id = 'G1'")
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_system_requirements(self):
        self.db.insert_system_requirements(
            None,
            "SR1",
            "Detect obstacles",
            "Mandatory",
            "Safety",
            "E.Z",
            "Reviewed",
            "E.Z",
        )
        self.db.cursor.execute(
            "SELECT * FROM system_requirements WHERE sys_req_id = 'SR1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_goal_children(self):
        self.db.insert_goal("G1", "Safety", "Operator", "Spec", "Key", "Critical")
        self.db.insert_system_requirements(
            None,
            "SR1",
            "Detect obstacles",
            "Mandatory",
            "Safety",
            "E.Z",
            "Reviewed",
            "E.Z",
        )
        self.db.insert_goal_children("G1", "SR1")
        self.db.cursor.execute(
            "SELECT * FROM goal_children WHERE goal_id = 'G1' AND sys_req_id = 'SR1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_subsystem_requirements(self):
        self.db.insert_subsystem_requirements(
            None, "SUB1", "Fly low", "Optional", "Stealth", "E.Z", "TBR", "E.Z"
        )
        self.db.cursor.execute(
            "SELECT * FROM subsystem_requirements WHERE sub_req_id = 'SUB1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_sysreq_children(self):
        self.db.insert_system_requirements(
            None,
            "SR1",
            "Detect obstacles",
            "Mandatory",
            "Safety",
            "E.Z",
            "Reviewed",
            "E.Z",
        )
        self.db.insert_subsystem_requirements(
            None, "SUB1", "Fly low", "Optional", "Stealth", "E.Z", "TBR", "E.Z"
        )
        self.db.insert_sysreq_children("SR1", "SUB1")
        self.db.cursor.execute(
            "SELECT * FROM sysreq_children WHERE sys_req_id = 'SR1' AND sub_req_id = 'SUB1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_item(self):
        self.db.insert_item("I1", "Camera")
        self.db.cursor.execute("SELECT * FROM item WHERE item_id = 'I1'")
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_sys_join_item(self):
        self.db.insert_item("I1", "Camera")
        self.db.insert_subsystem_requirements(
            None, "SUB1", "Fly low", "Optional", "Stealth", "E.Z", "TBR", "E.Z"
        )
        self.db.insert_sys_join_item("I1", "SUB1")
        self.db.cursor.execute(
            "SELECT * FROM sys_join_item WHERE item_id = 'I1' AND subsys_req_id = 'SUB1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_test_and_verification(self):
        self.db.insert_test_and_verification("M1", "Visual check", "Inspection")
        self.db.cursor.execute(
            "SELECT * FROM test_and_verification WHERE method_id = 'M1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_documents(self):
        self.db.cursor.execute("DROP TABLE documents")  # fix schema mismatch
        self.db.cursor.execute(
            """
            CREATE TABLE documents(
                doc_id VARCHAR PRIMARY KEY,
                title VARCHAR,
                description VARCHAR,
                file BLOB,
                version VARCHAR,
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H'))
            )
        """
        )
        self.db.insert_documents(
            "D1", "Spec Sheet", "Drone specs", b"PDFDATA", "v1.0", "E.Z"
        )
        self.db.cursor.execute("SELECT * FROM documents WHERE doc_id = 'D1'")
        self.assertIsNotNone(self.db.cursor.fetchone())

    def test_insert_V_join_documents(self):
        self.db.insert_test_and_verification("M1", "Visual check", "Inspection")
        self.db.cursor.execute(
            """
            INSERT INTO documents(doc_id, title, description, file, version, author)
            VALUES ('D1', 'Spec Sheet', 'Drone specs', ?, 'v1.0', 'E.Z')
        """,
            (b"PDFDATA",),
        )
        self.db.insert_V_join_documents("M1", "D1")
        self.db.cursor.execute(
            "SELECT * FROM V_join_documents WHERE method_id = 'M1' AND doc_id = 'D1'"
        )
        self.assertIsNotNone(self.db.cursor.fetchone())
