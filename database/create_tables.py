# create_tables.py

class create_tables:
    def __init__(self, cursor):
        self.cursor = cursor

    # ------------------ INTERNAL HELPER ------------------
    def _ensure(self, table_name: str, create_sql: str):
        """
        Create a table only if it does not already exist and print an accurate message.

        Parameters
        ----------
        table_name : str
            Name of the table to check in sqlite_master.
        create_sql : str
            Full CREATE TABLE statement.
        """
        exists = self.cursor.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        ).fetchone()

        if exists:
            print(f"Table '{table_name}' already exists (skipped).")
        else:
            self.cursor.execute(create_sql)
            print(f"Table '{table_name}' created successfully.")

    # ------------------ TABLES ------------------
    def create_goals_table(self):
        create_sql = """
        CREATE TABLE goals (
            goal_id VARCHAR PRIMARY KEY,
            goal_description VARCHAR NOT NULL,
            stakeholder VARCHAR,
            origin VARCHAR,
            priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
            rationale VARCHAR,
            satisfaction_status TEXT CHECK (satisfaction_status IN ('Pending','Not satisfied','Satisfied')),
            method_id VARCHAR,
            FOREIGN KEY (method_id) REFERENCES test_and_verification (method_id)
        )
        """
        self._ensure("goals", create_sql)
   
    def create_drone_swarm_requirements_table (self):
        create_sql = """
        CREATE TABLE drone_swarm_requirements (
            swarm_req_id VARCHAR PRIMARY KEY,
            requirement VARCHAR NOT NULL,
            priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
            effect VARCHAR NOT NULL,
            rationale VARCHAR,
            author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
            review_status TEXT CHECK (review_status IN ('TBR','Reviewed','Accepted', 'Rejected')),
            reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H','TBR')),
            verification_status TEXT CHECK (verification_status IN ('Pending','Failed','Verified','Inconclusive')),
            verification_method VARCHAR,
            comment VARCHAR,
            FOREIGN KEY (verification_method) REFERENCES test_and_verification (method_id)
        )
        """
        self._ensure("drone_swarm_requirements", create_sql)

    def create_goal_children_table(self):
        create_sql = """
        CREATE TABLE goal_children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id VARCHAR NOT NULL,
            swarm_req_id VARCHAR UNIQUE NOT NULL,
            FOREIGN KEY (goal_id) REFERENCES goals (goal_id),
            FOREIGN KEY (swarm_req_id) REFERENCES drone_swarm_requirements(swarm_req_id)
        )
        """
        self._ensure("goal_children", create_sql)

    def create_system_requirements_table(self):
        create_sql = """
        CREATE TABLE system_requirements (
            parent_id VARCHAR,
            sys_req_id VARCHAR PRIMARY KEY NOT NULL,
            requirement VARCHAR NOT NULL,
            priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
            effect VARCHAR NOT NULL,
            rationale VARCHAR,
            author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
            review_status TEXT CHECK (review_status IN ('TBR','Reviewed','Accepted', 'Rejected')),
            reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H','TBR')),
            verification_status TEXT CHECK (verification_status IN ('Pending','Failed','Verified','Inconclusive')),
            verification_method VARCHAR,
            comment VARCHAR,
            FOREIGN KEY (parent_id) REFERENCES system_requirements (sys_req_id), 
            FOREIGN KEY (verification_method) REFERENCES test_and_verification (method_id)     
        )
        """
        self._ensure("system_requirements", create_sql)

    def create_swarm_req_children_table(self):
        create_sql = """
        CREATE TABLE swarm_req_children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            swarm_req_id VARCHAR  NOT NULL,
            sys_req_id VARCHAR UNIQUE NOT NULL,
            FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id),
            FOREIGN KEY (swarm_req_id) REFERENCES drone_swarm_requirements (swarm_req_id)
        )
        """
        self._ensure("swarm_req_children", create_sql)

    def create_subsystem_requirements_table(self):
        create_sql = """
        CREATE TABLE subsystem_requirements (
            parent_id VARCHAR,
            sub_req_id VARCHAR PRIMARY KEY NOT NULL,
            requirement VARCHAR NOT NULL,
            priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
            effect VARCHAR NOT NULL,
            rationale VARCHAR,
            author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
            review_status TEXT CHECK (review_status IN ('TBR','Reviewed','Accepted', 'Rejected')),
            reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H','TBR')),
            verification_status TEXT CHECK (verification_status IN ('Pending','Failed','Verified','Inconclusive')),
            verification_method VARCHAR,
            comment VARCHAR,
            FOREIGN KEY (parent_id) REFERENCES subsystem_requirements (sub_req_id),
            FOREIGN KEY (verification_method) REFERENCES test_and_verification (method_id)     
        )
        """
        self._ensure("subsystem_requirements", create_sql)

    def create_sysreq_children_table(self):
        create_sql = """
        CREATE TABLE sysreq_children(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sys_req_id VARCHAR NOT NULL,
            sub_req_id VARCHAR UNIQUE NOT NULL,
            FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id),
            FOREIGN KEY (sub_req_id) REFERENCES subsystem_requirements (sub_req_id)
        )
        """
        self._ensure("sysreq_children", create_sql)

    def create_subsys_join_item_table(self):
        create_sql = """
        CREATE TABLE sys_join_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id VARCHAR NOT NULL,
            sub_req_id VARCHAR UNIQUE NOT NULL,   
            FOREIGN KEY (item_id) REFERENCES item (item_id),
            FOREIGN KEY (sub_req_id) REFERENCES subsystem_requirements (sub_req_id)                
        )
        """
        self._ensure("sys_join_item", create_sql)

    def create_item_table(self):
        create_sql = """
        CREATE TABLE item (
            item_id VARCHAR PRIMARY KEY NOT NULL,
            item_name VARCHAR NOT NULL
        )
        """
        self._ensure("item", create_sql)

    def create_documents_table(self):
        create_sql = """
        CREATE TABLE documents (
            doc_id VARCHAR PRIMARY KEY NOT NULL,
            title VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            file BLOB,
            version INTEGER,
            author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H'))   
        )
        """
        self._ensure("documents", create_sql)
         
    def create_test_and_verification_table (self):
        create_sql = """
        CREATE TABLE test_and_verification (
            method_id VARCHAR PRIMARY KEY NOT NULL,
            description VARCHAR NOT NULL,
            method_type TEXT CHECK (method_type IN ('Inspection','Analysis','Test'))    
        )
        """
        self._ensure("test_and_verification", create_sql)

    def create_V_join_documents_table(self):
        create_sql = """
        CREATE TABLE V_join_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_id VARCHAR NOT NULL,
            doc_id VARCHAR NOT NULL,  
            FOREIGN KEY (method_id) REFERENCES test_and_verification (method_id),
            FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
        )
        """
        self._ensure("V_join_documents", create_sql)

    def create_id_glossary_table(self):
        create_sql = """
        CREATE TABLE id_glossary (
            gloss_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefix VARCHAR NOT NULL,
            meaning VARCHAR NOT NULL  
        )
        """
        self._ensure("id_glossary", create_sql)

    def create_quality_requirements_table(self):
        create_sql = """
        CREATE TABLE quality_requirements (
            quality_rec_id VARCHAR PRIMARY KEY, 
            requirement VARCHAR, 
            author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
            approved_by TEXT CHECK (approved_by IN ('Y.M.B') OR approved_by IS NULL)
        )
        """
        self._ensure("quality_requirements", create_sql)
    
    def create_all_tables(self):
        # Create each table individually
        try:
            self.create_test_and_verification_table()
            self.create_documents_table()
            self.create_V_join_documents_table()
            self.create_id_glossary_table()
            self.create_quality_requirements_table()
            self.create_goals_table()
            self.create_goal_children_table()
            self.create_drone_swarm_requirements_table()
            self.create_system_requirements_table()
            self.create_subsystem_requirements_table()
            self.create_item_table()
            self.create_subsys_join_item_table()
            self.create_sysreq_children_table()
            self.create_swarm_req_children_table()
            
            print("\nAll required tables are present.")
        
        except Exception as e:
            print(f"Error creating tables: {e}")
