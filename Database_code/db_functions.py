import sqlite3


class req_database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign keys
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def create_goals_table(self):
        self.cursor.execute(
            """
            CREATE TABLE goals (
            goal_id VARCHAR PRIMARY KEY,
            goal_description VARCHAR NOT NULL,
            stakeholder VARCHAR,
            origin VARCHAR,
            priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
            rationale varchar
            )
            """
        )

    def create_goal_children_table(self):
        self.cursor.execute(
            """
                CREATE TABLE goal_children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id VARCHAR NOT NULL,
                sys_req_id VARCHAR UNIQUE NOT NULL,
                FOREIGN KEY (goal_id) REFERENCES goals (goal_id) ON DELETE CASCADE,
                FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id) ON DELETE CASCADE
                )
                """
        )

    def create_system_requirements_table(self):
        self.cursor.execute(
            """
                CREATE TABLE system_requirements(
                parent_id VARCHAR,
                sys_req_id VARCHAR PRIMARY KEY NOT NULL,
                requirement VARCHAR NOT NULL,
                priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
                effect VARCHAR NOT NULL,
                review_status TEXT CHECK (review_status IN ('TBR','Reviewed')),
                reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H',"")),
                author TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H',"")),
                FOREIGN KEY (parent_id) REFERENCES system_requirements (sys_req_id)ON DELETE CASCADE      
                )
                """
        )

    def create_subsystem_requirements_table(self):
        self.cursor.execute(
            """
                CREATE TABLE subsystem_requirements(
                parent_id VARCHAR,
                sub_req_id VARCHAR PRIMARY KEY NOT NULL,
                requirement VARCHAR NOT NULL,
                priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
                effect VARCHAR NOT NULL,
                review_status TEXT CHECK (review_status IN ('TBR','Reviewed')),
                reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H',"")),
                author TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H',"")), 
                FOREIGN KEY (parent_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE
                )
                """
        )

    def create_sysreq_children_table(self):
        self.cursor.execute(
            """
                CREATE TABLE sysreq_children(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sys_req_id VARCHAR NOT NULL,
                sub_req_id VARCHAR NOT NULL,
                FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id) ON DELETE CASCADE ,
                FOREIGN KEY (sub_req_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE
                )
              """
        )

    def create_sys_join_item_table(self):
        self.cursor.execute(
            """
                CREATE TABLE sys_join_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id VARCHAR NOT NULL,
                subsys_req_id VARCHAR NOT NULL,   
                FOREIGN KEY (item_id) REFERENCES item (item_id) ON DELETE CASCADE ,
                FOREIGN KEY (subsys_req_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE                
                )
                """
        )

    def create_item_table(self):
        self.cursor.execute(
            """
                CREATE TABLE item (
                item_id VARCHAR PRIMARY KEY NOT NULL,
                item_name VARCHAR NOT NULL
                )
                """
        )

    def create_documents_table(self):
        self.cursor.execute(
            """
                CREATE TABLE documents(
                doc_id VARCHAR PRIMARY KEY NOT NULL,
                title VARCHAR NOT NULL,
                description VARCHAR NOT NULL,
                file LONGBLOB,
                version INTEGER,
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H') )   
                )
                """
        )

    def create_test_and_verification_table(self):
        self.cursor.execute(
            """
                CREATE TABLE test_and_verification (
                method_id VARCHAR PRIMARY KEY NOT NULL,
                description VARCHAR NOT NULL,
                method_type TEXT CHECK (method_type IN ('Inspection','Analysis','Test'))    
                )
                """
        )

    def create_V_join_documents(self):
        self.cursor.execute(
            """
                CREATE TABLE V_join_documents(
                method_id VARCHAR NOT NULL,
                doc_id VARCHAR NOT NULL,  
                FOREIGN KEY (method_id) REFERENCES test_and_verification (method_id) ON DELETE CASCADE,
                FOREIGN KEY (doc_id) REFERENCES documents (doc_id) ON DELETE CASCADE
                )
                """
        )

    def create_quality_requirements(self):
        self.cursor.execute(
            """
                CREATE TABLE Quality_Requirements(
                id VARCHAR PRIMARY KEY, 
                requirement VARCHAR, 
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
                approved_by TEXT CHECK (approved_by IN ('Y.M.B'))       
                )
                """
        )

    def create_all_tables(self):
        self.create_goals_table()
        self.create_system_requirements_table()
        self.create_goal_children_table()
        self.create_item_table()
        self.create_sys_join_item_table()
        self.create_subsystem_requirements_table()
        self.create_sysreq_children_table()
        self.create_test_and_verification_table()
        self.create_documents_table()
        self.create_V_join_documents()
        self.create_quality_requirements()

    def insert_goal(
        self, goal_id, goal_description, stakeholder, origin, priority, rationale
    ):
        self.cursor.execute(
            """
            INSERT INTO goals (goal_id, goal_description, stakeholder, origin, priority, rationale)
            VALUES (?,?,?,?,?,?)
            """,
            (goal_id, goal_description, stakeholder, origin, priority, rationale),
        )

    def insert_system_requirements(
        self,
        parent_id,
        sys_req_id,
        requirement,
        priority,
        effect,
        author,
        review_status,
        reviewer,
    ):
        self.cursor.execute(
            """
            INSERT INTO system_requirements (parent_id, sys_req_id,requirement,priority,effect,author,review_status,reviewer)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                parent_id,
                sys_req_id,
                requirement,
                priority,
                effect,
                author,
                review_status,
                reviewer,
            ),
        )

    def insert_goal_children(self, goal_id, sys_req_id):
        self.cursor.execute(
            """
            INSERT INTO goal_children (goal_id, sys_req_id)
            VALUES (?,?)
            """,
            (goal_id, sys_req_id),
        )

    def insert_subsystem_requirements(
        self,
        parent_id,
        sub_req_id,
        requirement,
        priority,
        effect,
        author,
        review_status,
        reviewer,
    ):
        self.cursor.execute(
            """
            INSERT INTO subsystem_requirements (parent_id, sub_req_id,requirement,priority,effect,author,review_status,reviewer)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                parent_id,
                sub_req_id,
                requirement,
                priority,
                effect,
                author,
                review_status,
                reviewer,
            ),
        )

    def insert_sysreq_children(self, sys_req_id, sub_req_id):
        self.cursor.execute(
            """
            INSERT INTO sysreq_children (sys_req_id, sub_req_id)
            VALUES (?,?)
            """,
            (sys_req_id, sub_req_id),
        )

    def insert_item(self, item_id, item_name):
        self.cursor.execute(
            """
            INSERT INTO item (item_id, item_name)
            VALUES (?,?)
            """,
            (item_id, item_name),
        )

    def insert_sys_join_item(self, item_id, susbsys_req_id):
        self.cursor.execute(
            """
            INSERT INTO sys_join_item (item_id, subsys_req_id)
            VALUES (?,?)
            """,
            (item_id, susbsys_req_id),
        )

    def insert_test_and_verification(self, method_id, description, method_type):
        self.cursor.execute(
            """
            INSERT INTO test_and_verification (method_id, description, method_type)
            VALUES (?,?,?)
            """,
            (method_id, description, method_type),
        )

    def insert_documents(self, doc_id, title, description, file, version, author):
        self.cursor.execute(
            """
            INSERT INTO documents (doc_id,title, description, file, version,author)
            VALUES (?,?,?,?,?,?)
            """,
            (doc_id, title, description, file, version, author),
        )

    def insert_V_join_documents(self, method_id, doc_id):
        self.cursor.execute(
            """
            INSERT INTO V_join_documents (method_id, doc_id)
            VALUES (?,?)
            """,
            (method_id, doc_id),
        )
# db_name = "test.db"

# with req_database (db_name) as db:
#     #db.create_all_tables ()
#     db.insert_subsystem_requirements(None,"SUB01","This requirement shall test the db function","Key","Results","C.N","TBR","")

