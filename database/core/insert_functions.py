# insert_functions.py

class insert_functions:
    def __init__(self, cursor, conn=None):
        # Accept the connection so we can serialize writers when generating IDs.
        self.cursor = cursor
        self.conn = conn
    
    # --- ID generator ---
    def _next_id(self, table: str, col: str, prefix: str, width: int = 2) -> str:
        """
        Mint the next ID like 'G-01', 'SW-02', etc.
        Uses BEGIN IMMEDIATE to avoid two writers picking the same number.
        """
        if self.conn:
            self.conn.execute("BEGIN IMMEDIATE")
        # Find the highest numeric suffix currently present for this prefix
        row = self.cursor.execute(
            f"""
            SELECT {col}
            FROM {table}
            WHERE {col} LIKE ? || '-%'
            ORDER BY CAST(SUBSTR({col}, LENGTH(?)+2) AS INTEGER) DESC
            LIMIT 1
            """,
            (prefix, prefix)
        ).fetchone()
        nxt = (int(row[0].split('-')[1]) + 1) if row else 1
        return f"{prefix}-{str(nxt).zfill(width)}"

    # --- Validation helpers ---
    def validate_author_reviewer(self, author, reviewer):
        if author == reviewer:
            raise ValueError("Author and reviewer must be different to ensure unbiased review.")

    def validate_verification(self, verification_status, verification_method):
        if verification_status != "Pending" and not verification_method:
            raise ValueError("Verification method must be provided if status is not pending.")

    # --- Insert methods ---
    def insert_goal(self, goal_id, goal_description, stakeholder, origin, priority, rationale, satisfaction_status, method_id=None):
        if not goal_id:
            goal_id = self._next_id("goals", "goal_id", "G", width=2)
        self.cursor.execute(
            """
            INSERT INTO goals 
            (goal_id, goal_description, stakeholder, origin, priority, rationale, satisfaction_status, method_id)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (goal_id, goal_description, stakeholder, origin, priority, rationale, satisfaction_status, method_id)
        )

    def insert_drone_swarm_requirements(self, swarm_req_id, requirement, priority, effect, rationale,
                                        author, review_status, reviewer, verification_status,
                                        verification_method=None, comment=None):
        self.validate_author_reviewer(author, reviewer)
        self.validate_verification(verification_status, verification_method)
        if not swarm_req_id:
            swarm_req_id = self._next_id("drone_swarm_requirements", "swarm_req_id", "SW", width=2)
        self.cursor.execute(
            """
            INSERT INTO drone_swarm_requirements
            (swarm_req_id, requirement, priority, effect, rationale, author, review_status, reviewer, verification_status, verification_method, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (swarm_req_id, requirement, priority, effect, rationale, author, review_status, reviewer, verification_status, verification_method, comment)
        )

    def insert_system_requirements(self, parent_id, sys_req_id, requirement, priority, effect, rationale,
                                   author, review_status, reviewer, verification_status,
                                   verification_method=None, comment=None):
        self.validate_author_reviewer(author, reviewer)
        self.validate_verification(verification_status, verification_method)
        if not sys_req_id:
            sys_req_id = self._next_id("system_requirements", "sys_req_id", "SYS", width=2)
        self.cursor.execute(
            """
            INSERT INTO system_requirements
            (parent_id, sys_req_id, requirement, priority, effect, rationale, author, review_status, reviewer, verification_status, verification_method, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (parent_id, sys_req_id, requirement, priority, effect, rationale, author, review_status, reviewer, verification_status, verification_method, comment)
        )

    def insert_goal_children(self, goal_id, swarm_req_id):
        self.cursor.execute(
            """
            INSERT INTO goal_children (goal_id, swarm_req_id)
            VALUES (?,?)
            """,
            (goal_id, swarm_req_id)
        )

    def insert_swarm_req_children(self, swarm_req_id, sys_req_id):
        self.cursor.execute(
            """
            INSERT INTO swarm_req_children (swarm_req_id, sys_req_id)
            VALUES (?,?)
            """,
            (swarm_req_id, sys_req_id)
        )

    def insert_subsystem_requirements(self, parent_id, sub_req_id, requirement, priority, effect, rationale,
                                      author, review_status, reviewer, verification_status,
                                      verification_method=None, comment=None):
        self.validate_author_reviewer(author, reviewer)
        self.validate_verification(verification_status, verification_method)
        if not sub_req_id:
            sub_req_id = self._next_id("subsystem_requirements", "sub_req_id", "SS", width=2)
        self.cursor.execute(
            """
            INSERT INTO subsystem_requirements
            (parent_id, sub_req_id, requirement, priority, effect, rationale, author, review_status, reviewer, verification_status, verification_method, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (parent_id, sub_req_id, requirement, priority, effect, rationale, author, review_status, reviewer, verification_status, verification_method, comment)
        )

    def insert_sysreq_children(self, sys_req_id, sub_req_id):
        self.cursor.execute(
            """
            INSERT INTO sysreq_children (sys_req_id, sub_req_id)
            VALUES (?,?)
            """,
            (sys_req_id, sub_req_id)
        )

    def insert_item(self, item_id, item_name):
        if not item_id:
            item_id = self._next_id("items", "item_id", "I", width=2)
        self.cursor.execute(
            """
            INSERT INTO item (item_id, item_name)
            VALUES (?,?)
            """,
            (item_id, item_name)
        )

    def insert_subsys_join_item(self, item_id, sub_req_id):
        self.cursor.execute(
            """
            INSERT INTO sys_join_item (item_id, sub_req_id)
            VALUES (?,?)
            """,
            (item_id, sub_req_id)
        )

    def insert_test_and_verification(self, method_id, description, method_type):
        if not method_id:
            method_id = self._next_id("test_and_verification", "method_id", "M", width=2)
        self.cursor.execute(
            """
            INSERT INTO test_and_verification (method_id, description, method_type)
            VALUES (?,?,?)
            """,
            (method_id, description, method_type)
        )

    def insert_documents(self, doc_id, title, description, file=None, version=None, author=None):
        if not doc_id:
            doc_id = self._next_id("documents", "doc_id", "D", width=2)
        self.cursor.execute(
            """
            INSERT INTO documents (doc_id, title, description, file, version, author)
            VALUES (?,?,?,?,?,?)
            """,
            (doc_id, title, description, file, version, author)
        )

    def insert_V_join_documents(self, method_id, doc_id):
        self.cursor.execute(
            """
            INSERT INTO V_join_documents (method_id, doc_id)
            VALUES (?,?)
            """,
            (method_id, doc_id)
        )

    def insert_id_glossary(self, prefix, meaning):
        self.cursor.execute(
            """
            INSERT INTO id_glossary (prefix, meaning)
            VALUES (?,?)
            """,
            (prefix, meaning)
        )

    def insert_quality_requirements(self, quality_rec_id, requirement, author, approved_by=None):
        if not quality_rec_id:
            quality_rec_id = self._next_id("quality_requirements", "quality_rec_id", "QR", width=2)
        self.cursor.execute(
            """
            INSERT INTO quality_requirements (quality_rec_id, requirement, author, approved_by)
            VALUES (?,?,?,?)
            """,
            (quality_rec_id, requirement, author, approved_by)
        )
