# insert_functions.py

class insert_functions:
    def __init__(self, cursor, conn=None):
        self.cursor = cursor
        self.conn = conn

        # --- centralized prefix map ---
        # table_name : (prefix, zero_padding_width)
        self.PREFIX_INFO = {
            "goals": ("G", 2),
            "drone_swarm_requirements": ("SW", 2),
            "system_requirements": ("SYS", 2),
            "subsystem_requirements": ("SS", 2),
            "items": ("I", 2),
            "test_and_verification": ("M", 2),
            "documents": ("D", 2),
            "quality_requirements": ("QR", 2)
        }

    # --- internal helper to generate next ID ---
    def _next_id(self, table: str, col: str) -> str:
        """
        Mint the next ID like 'G-01', 'SYS-02', etc.
        Looks up prefix and padding width automatically from PREFIX_INFO.
        Uses BEGIN IMMEDIATE to avoid two writers grabbing the same number.
        """
        prefix, width = self.PREFIX_INFO.get(table, ("X", 2))

        if self.conn:
            self.conn.execute("BEGIN IMMEDIATE")

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

    # --- insert functions below (unchanged except for ID handling) ---
    def insert_goal(self, goal_id, goal_description, stakeholder, origin,
                    priority, rationale, satisfaction_status, method_id=None):
        if not goal_id:
            goal_id = self._next_id("goals", "goal_id")
        self.cursor.execute(
            """
            INSERT INTO goals
            (goal_id, goal_description, stakeholder, origin, priority, rationale,
             satisfaction_status, method_id)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (goal_id, goal_description, stakeholder, origin, priority,
             rationale, satisfaction_status, method_id)
        )

    def insert_drone_swarm_requirements(self, swarm_req_id, requirement, priority,
                                        effect, rationale, author, review_status,
                                        reviewer, verification_status, verification_method=None, comment=None):
        if not swarm_req_id:
            swarm_req_id = self._next_id("drone_swarm_requirements", "swarm_req_id")
        self.cursor.execute(
            """
            INSERT INTO drone_swarm_requirements
            (swarm_req_id, requirement, priority, effect, rationale, author,
             review_status, reviewer, verification_status, verification_method, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (swarm_req_id, requirement, priority, effect, rationale, author,
             review_status, reviewer, verification_status, verification_method, comment)
        )

    def insert_system_requirements(self, parent_id, sys_req_id, requirement,
                                   priority, effect, rationale, author, review_status,
                                   reviewer, verification_status, verification_method=None, comment=None):
        if not sys_req_id:
            sys_req_id = self._next_id("system_requirements", "sys_req_id")
        self.cursor.execute(
            """
            INSERT INTO system_requirements
            (parent_id, sys_req_id, requirement, priority, effect, rationale, author,
             review_status, reviewer, verification_status, verification_method, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (parent_id, sys_req_id, requirement, priority, effect, rationale, author,
             review_status, reviewer, verification_status, verification_method, comment)
        )

    def insert_subsystem_requirements(self, parent_id, sub_req_id, requirement,
                                      priority, effect, rationale, author, review_status,
                                      reviewer, verification_status, verification_method=None, comment=None):
        if not sub_req_id:
            sub_req_id = self._next_id("subsystem_requirements", "sub_req_id")
        self.cursor.execute(
            """
            INSERT INTO subsystem_requirements
            (parent_id, sub_req_id, requirement, priority, effect, rationale, author,
             review_status, reviewer, verification_status, verification_method, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (parent_id, sub_req_id, requirement, priority, effect, rationale, author,
             review_status, reviewer, verification_status, verification_method, comment)
        )

    def insert_item(self, item_id, name, specification, allocated_to=None):
        if not item_id:
            item_id = self._next_id("items", "item_id")
        self.cursor.execute(
            "INSERT INTO items (item_id, name, specification, allocated_to) VALUES (?,?,?,?)",
            (item_id, name, specification, allocated_to)
        )

    def insert_test_and_verification(self, method_id, description, method_type):
        if not method_id:
            method_id = self._next_id("test_and_verification", "method_id")
        self.cursor.execute(
            "INSERT INTO test_and_verification (method_id, description, method_type) VALUES (?,?,?)",
            (method_id, description, method_type)
        )

    def insert_documents(self, doc_id, title, description, file=None, version=None, author=None):
        if not doc_id:
            doc_id = self._next_id("documents", "doc_id")
        self.cursor.execute(
            "INSERT INTO documents (doc_id, title, description, file, version, author) VALUES (?,?,?,?,?,?)",
            (doc_id, title, description, file, version, author)
        )

    def insert_quality_requirements(self, quality_rec_id, requirement, author, approved_by=None):
        if not quality_rec_id:
            quality_rec_id = self._next_id("quality_requirements", "quality_rec_id")
        self.cursor.execute(
            "INSERT INTO quality_requirements (quality_rec_id, requirement, author, approved_by) VALUES (?,?,?,?)",
            (quality_rec_id, requirement, author, approved_by)
        )
