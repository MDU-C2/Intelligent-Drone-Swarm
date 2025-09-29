# create_tables.py

class create_tables:
    def __init__(self, cursor):
        self.cursor = cursor

    # ------------------ TABLES ------------------
    def create_goals_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS goals (
                goal_id VARCHAR PRIMARY KEY,
                goal_description VARCHAR NOT NULL,
                stakeholder VARCHAR,
                origin VARCHAR,
                priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
                rationale varchar,
                satisfaction_status TEXT CHECK (satisfaction_status IN ('Pending','Not satisfied','Satisfied')),
                method_id VARCHAR,
                FOREIGN KEY (method_id) REFERENCES test_and_verification (method_id)
            )
            """
        )
   
    def create_drone_swarm_requirements_table (self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS drone_swarm_requirements (
                swarm_req_id VARCHAR PRIMARY KEY,
                requirement VARCHAR NOT NULL,
                priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
                effect VARCHAR NOT NULL,
                rationale VARCHAR,
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
                review_status TEXT CHECK (review_status IN ('TBR','Reviewed','Accepted', 'Rejected')),
                reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H',"TBR")),
                verification_status TEXT CHECK (verification_status IN ('Pending','Failed','Verified','Inconclusive')),
                verification_method VARCHAR,
                comment VARCHAR,
                FOREIGN KEY (verification_method) REFERENCES test_and_verification (method_id)
            )
            """
        )

    def create_goal_children_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS goal_children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id VARCHAR NOT NULL,
                swarm_req_id VARCHAR UNIQUE NOT NULL,
                FOREIGN KEY (goal_id) REFERENCES goals (goal_id) ON DELETE CASCADE
            )
            """
        )

    def create_system_requirements_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_requirements (
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
                FOREIGN KEY (parent_id) REFERENCES system_requirements (sys_req_id) ON DELETE CASCADE, 
                FOREIGN KEY (verification_method) REFERENCES test_and_verification (method_id)     
            )
            """
        )

    def create_swarm_req_children_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS swarm_req_children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                swarm_req_id VARCHAR  NOT NULL,
                sys_req_id VARCHAR UNIQUE NOT NULL,
                FOREIGN KEY (sys_req_id) REFERENCES system_requirements  (sys_req_id) ON DELETE CASCADE,
                FOREIGN KEY (swarm_req_id) REFERENCES drone_swarm_requirements (swarm_req_id) ON DELETE CASCADE
            )
            """
        )

    def create_subsystem_requirements_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subsystem_requirements (
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
                FOREIGN KEY (parent_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE,
                FOREIGN KEY (verification_method) REFERENCES test_and_verification (method_id)     
            )
            """
        )

    def create_sysreq_children_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sysreq_children(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sys_req_id VARCHAR NOT NULL,
                sub_req_id VARCHAR NOT NULL,
                FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id) ON DELETE CASCADE,
                FOREIGN KEY (sub_req_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE
            )
            """
        )

    def create_subsys_join_item_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sys_join_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id VARCHAR NOT NULL,
                sub_req_id VARCHAR NOT NULL,   
                FOREIGN KEY (item_id) REFERENCES item (item_id) ON DELETE CASCADE,
                FOREIGN KEY (sub_req_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE                
            )
            """
        )

    def create_item_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS item (
                item_id VARCHAR PRIMARY KEY NOT NULL,
                item_name VARCHAR NOT NULL
            )
            """
        )

    def create_documents_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                doc_id VARCHAR PRIMARY KEY NOT NULL,
                title VARCHAR NOT NULL,
                description VARCHAR NOT NULL,
                file LONGBLOB,
                version INTEGER,
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H'))   
            )
            """
        ) 
         
    def create_test_and_verification_table (self):
         self.cursor.execute (
            """
            CREATE TABLE IF NOT EXISTS test_and_verification (
                method_id VARCHAR PRIMARY KEY NOT NULL,
                description VARCHAR NOT NULL,
                method_type TEXT CHECK (method_type IN ('Inspection','Analysis','Test'))    
            )
            """
        )

    def create_V_join_documents_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS V_join_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method_id VARCHAR NOT NULL,
                doc_id VARCHAR NOT NULL,  
                FOREIGN KEY (method_id) REFERENCES test_and_verification (method_id) ON DELETE CASCADE,
                FOREIGN KEY (doc_id) REFERENCES documents (doc_id) ON DELETE CASCADE
            )
            """
        )

    def create_id_glossary_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS id_glossary (
                gloss_id INTEGER PRIMARY KEY AUTOINCREMENT,
                prefix VARCHAR NOT NULL,
                meaning VARCHAR NOT NULL  
            )
            """
        )

    def create_quality_requirements_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Quality_Requirements (
                quality_rec_id VARCHAR PRIMARY KEY, 
                requirement VARCHAR, 
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
                approved_by TEXT CHECK (approved_by IN ('Y.M.B',''))       
            )
            """
        )
    
    def create_all_tables(self):
        # Create each table individually with success messages
        # Change message depending on IF EXIST
        try:
            self.create_test_and_verification_table()
            print("Table 'test_and_verification' created successfully.")
            
            self.create_documents_table()
            print("Table 'documents' created successfully.")
            
            self.create_V_join_documents_table()
            print("Table 'V_join_documents' created successfully.")
            
            self.create_id_glossary_table()
            print("Table 'id_glossary' created successfully.")
            
            self.create_quality_requirements_table()
            print("Table 'quality_requirements' created successfully.")
            
            self.create_goals_table()
            print("Table 'goals' created successfully.")
            
            self.create_goal_children_table()
            print("Table 'goal_children' created successfully.")
            
            self.create_drone_swarm_requirements_table()
            print("Table 'drone_swarm_requirements' created successfully.")
            
            self.create_system_requirements_table()
            print("Table 'system_requirements' created successfully.")
            
            self.create_subsystem_requirements_table()
            print("Table 'subsystem_requirements' created successfully.")
            
            self.create_item_table()
            print("Table 'item' created successfully.")
            
            self.create_subsys_join_item_table()
            print("Table 'sys_join_item' created successfully.")
            
            self.create_sysreq_children_table()
            print("Table 'sysreq_children' created successfully.")
            
            self.create_swarm_req_children_table()
            print("Table 'swarm_req_children' created successfully.")
            
            print("\nAll tables created successfully!")
        
        except Exception as e:
            print(f"Error creating tables: {e}")
