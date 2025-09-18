import sqlite3

class req_database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect (self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign keys        
        return  self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def create_goals_table (self):
            self.cursor.execute (
            """
            CREATE TABLE goals (
            goal_id VARCHAR PRIMARY KEY,
            goal_description VARCHAR,
            stakeholder VARCHAR,
            origin VARCHAR,
            priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
            rationale varchar
            )
            """
            )

    def create_goal_children_table (self):
            self.cursor.execute (
                """
                CREATE TABLE goal_children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id VARCHAR,
                sys_req_id VARCHAR UNIQUE,
                FOREIGN KEY (goal_id) REFERENCES goals (goal_id) ON DELETE CASCADE,
                FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id) ON DELETE CASCADE
                )
                """
                )
            
    def create_system_requirements_table (self):  
            self.cursor.execute (
                """
                CREATE TABLE system_requirements(
                parent_id VARCHAR,
                sys_req_id VARCHAR PRIMARY KEY,
                requirement VARCHAR,
                priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
                effect VARCHAR,
                review_status TEXT CHECK (review_status IN ('TBR','Reviewed')),
                reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
                author TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
                FOREIGN KEY (parent_id) REFERENCES system_requirements (sys_req_id)ON DELETE CASCADE      
                )
                """
                )
    
    def create_subsystem_requirements_table (self):  
            self.cursor.execute (
                """
                CREATE TABLE subsystem_requirements(
                parent_id VARCHAR,
                sub_req_id VARCHAR PRIMARY KEY,
                requirement VARCHAR,
                priority TEXT CHECK (priority IN ('Key','Mandatory','Optional')),
                effect VARCHAR,
                review_status TEXT CHECK (review_status IN ('TBR','Reviewed')),
                reviewer TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H')),
                author TEXT CHECK (reviewer IN ('E.Z','C.N','Y.M.B','E.M','A.H')), 
                FOREIGN KEY (parent_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE
                )
                """
                )

    def create_sysreq_children_table (self):
        self.cursor.execute (
              """
                CREATE TABLE sysreq_children(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sys_req_id VARCHAR,
                sub_req_id VARCHAR,
                FOREIGN KEY (sys_req_id) REFERENCES system_requirements (sys_req_id) ON DELETE CASCADE ,
                FOREIGN KEY (sub_req_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE
                )
              """  
               )  
    def create_sys_join_item_table (self):
         self.cursor.execute (
                """
                CREATE TABLE sys_join_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id VARCHAR,
                subsys_req_id VARCHAR,   
                FOREIGN KEY (item_id) REFERENCES item (item_id) ON DELETE CASCADE ,
                FOREIGN KEY (subsys_req_id) REFERENCES subsystem_requirements (sub_req_id) ON DELETE CASCADE                
                )
                """ )        

    def create_item_table (self):
         self.cursor.execute (
                """
                CREATE TABLE item (
                item_id VARCHAR PRIMARY KEY,
                item_name VARCHAR 
                )
                """
                )          

    def create_documents_table (self):
         self.cursor.execute (
                """
                CREATE TABLE documents(
                doc_id VARCHAR PRIMARY KEY,
                title VARCHAR ,
                description VARCHAR,
                file LONGBLOB,
                author TEXT CHECK (author IN ('E.Z','C.N','Y.M.B','E.M','A.H') )   
                )
                """
                ) 
         
    def create_test_and_verification_table (self):
         self.cursor.execute (
                """
                CREATE TABLE test_and_verification(
                method_id VARCHAR PRIMARY KEY,
                description VARCHAR,
                method_type TEXT CHECK (method_type IN ('Inspection','Analysis','Test')),
                document_id VARCHAR       
                )
                """
                )    
    
    def create_V_join_documents(self):
        self.cursor.execute (
                """
                CREATE TABLE V_join_documents(
                method_id VARCHAR,
                doc_id VARCHAR,  
                FOREIGN KEY (method_id) REFERENCES test_and_verification (method_id) ON DELETE CASCADE,
                FOREIGN KEY (doc_id) REFERENCES documents (doc_id) ON DELETE CASCADE
                )
                """
                )    
    def create_all_tables(self):
         self.create_goals_table ()
         self.create_system_requirements_table ()
         self.create_goal_children_table ()
         self.create_item_table ()
         self.create_sys_join_item_table ()
         self.create_subsystem_requirements_table ()
         self.create_sysreq_children_table ()
         self.create_test_and_verification_table ()
         self.create_documents_table ()
         self.create_V_join_documents ()
        
    def insert_goal (self, goal_id, goal_description, stakeholder, origin, priority,rationale):
            self.cursor.execute (
            """
            INSERT INTO goals (goal_id, goal_description, stakeholder, origin, priority, rationale)
            VALUES (?,?,?,?,?,?)
            """, (goal_id, goal_description, stakeholder, origin, priority, rationale)
            )



# db_name = "test.db"

# with req_database (db_name) as db:
     
#      #db.create_documents_table()
#      #db.create_item_table ()
#      #db.create_goal_children_table ()
#      #db.create_goals_table
#      #db.create_subsystem_requirements_table ()
#      #db.create_sys_join_item_table ()
#      #db.create_test_and_verification_table ()
#      #db.create_V_join_documents ()
#      #db.create_system_requirements_table


