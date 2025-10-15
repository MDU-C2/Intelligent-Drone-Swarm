# prompts.py

import sqlite3
from database.core.paths import DB_NAME_TXT

def prompt_input(prompt_text, optional=False):
    """Helper to allow typing 'exit' to cancel"""
    value = input(prompt_text)
    if value.lower() == "exit":
        return "EXIT"
    if optional and value == "":
        return None
    return value

# ----- PROMPTS FOR ALL TABLES -----
def prompt_goal():
    print("\nEnter new goal (type 'exit' to cancel):")

    goal_id = prompt_input("Goal ID (leave blank for auto): ", optional=True)
    if goal_id == "EXIT": return None

    goal_description = prompt_input("Description: ")
    if goal_description == "EXIT": return None

    stakeholder = prompt_input("Stakeholder: ")
    if stakeholder == "EXIT": return None

    origin = prompt_input("Origin: ")
    if origin == "EXIT": return None

    priority = prompt_input("Priority (Key/Mandatory/Optional): ")
    if priority == "EXIT": return None

    rationale = prompt_input("Rationale: ")
    if rationale == "EXIT": return None

    satisfaction_status = prompt_input("Satisfaction status (Pending/Not satisfied/Satisfied): ")
    if satisfaction_status == "EXIT": return None

    method_id = prompt_input("Method ID (optional): ", optional=True)
    if method_id == "EXIT": return None

    return {
        "goal_id": goal_id,
        "goal_description": goal_description,
        "stakeholder": stakeholder,
        "origin": origin,
        "priority": priority,
        "rationale": rationale,
        "satisfaction_status": satisfaction_status,
        "method_id": method_id,
    }

def prompt_drone_swarm_requirement():
    print("\nEnter new drone swarm requirement (type 'exit' to cancel):")
    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H): ")
    if author == "EXIT": return None
    reviewer = prompt_input("Reviewer (different from author (TBR allowed)): ")
    if reviewer == "EXIT": return None
    verification_status = prompt_input("Verification status (Pending/Failed/Verified/Inconclusive): ")
    if verification_status == "EXIT": return None
    verification_method = prompt_input("Verification method ID (optional): ", optional=True)
    if verification_method == "EXIT": return None

    data = {
        "swarm_req_id": prompt_input("Swarm Req ID (leave blank for auto): ", optional=True),
        "requirement": prompt_input("Requirement description: "),
        "priority": prompt_input("Priority (Key/Mandatory/Optional): "),
        "effect": prompt_input("Effect: "),
        "rationale": prompt_input("Rationale: "),
        "author": author,
        "review_status": prompt_input("Review status (TBR/Reviewed/Accepted/Rejected): "),
        "reviewer": reviewer,
        "verification_status": verification_status,
        "verification_method": verification_method,
        "comment": prompt_input("Comment (optional): ", optional=True)
    }
    if "EXIT" in data.values(): return None
    return data

def prompt_system_requirement():
    print("\nEnter System Requirement (type 'exit' to cancel):")
    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H): ")
    if author == "EXIT": return None
    reviewer = prompt_input("Reviewer (different from author (TBR allowed)): ")
    if reviewer == "EXIT": return None
    verification_status = prompt_input("Verification status (Pending/Failed/Verified/Inconclusive): ")
    if verification_status == "EXIT": return None
    verification_method = prompt_input("Verification method ID (optional): ", optional=True)
    if verification_method == "EXIT": return None

    data = {
        "parent_id": prompt_input("PARENT System Req ID: "),
        "sys_req_id": prompt_input("System Req ID (leave blank for auto): ", optional=True),
        "requirement": prompt_input("Requirement description: "),
        "priority": prompt_input("Priority (Key/Mandatory/Optional): "),
        "effect": prompt_input("Effect: "),
        "rationale": prompt_input("Rationale: "),
        "author": author,
        "review_status": prompt_input("Review status (TBR/Reviewed/Accepted/Rejected): "),
        "reviewer": reviewer,
        "verification_status": verification_status,
        "verification_method": verification_method,
        "comment": prompt_input("Comment (optional): ", optional=True)
    }
    if "EXIT" in data.values(): return None
    return data

def prompt_subsystem_requirement():
    print("\nEnter Subsystem Requirement (type 'exit' to cancel):")

    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H): ")
    if author == "EXIT": return None
    reviewer = prompt_input("Reviewer (different from author (TBR allowed)): ")
    if reviewer == "EXIT": return None
    verification_status = prompt_input("Verification status (Pending/Failed/Verified/Inconclusive): ")
    if verification_status == "EXIT": return None
    verification_method = prompt_input("Verification method ID (optional): ", optional=True)
    if verification_method == "EXIT": return None

    data = {
        "parent_id": prompt_input("PARENT Subsystem Req ID (optional): ", optional=True),
        "sub_req_id": prompt_input("Subsystem Req ID (leave blank for auto): ", optional=True),
        "requirement": prompt_input("Requirement description: "),
        "priority": prompt_input("Priority (Key/Mandatory/Optional): "),
        "effect": prompt_input("Effect: "),
        "rationale": prompt_input("Rationale (optional): ", optional=True),
        "author": author,
        "review_status": prompt_input("Review status (TBR/Reviewed/Accepted/Rejected): "),
        "reviewer": reviewer,
        "verification_status": verification_status,
        "verification_method": verification_method,
        "comment": prompt_input("Comment (optional): ", optional=True)
    }
    if "EXIT" in data.values(): return None
    return data

def prompt_goal_children():
    print("\nLink goal and swarm requirement (goal_children table (type 'exit' to cancel)):")
    goal_id = prompt_input("Goal ID: ")
    if goal_id == "EXIT": return None
    swarm_req_id = prompt_input("Swarm Req ID: ")
    if swarm_req_id == "EXIT": return None
    return {"goal_id": goal_id, "swarm_req_id": swarm_req_id}

def prompt_swarm_req_children():
    print("\nLink swarm requirement and system requirement (swarm_req_children table (type 'exit' to cancel)):")
    swarm_req_id = prompt_input("Swarm Req ID: ")
    if swarm_req_id == "EXIT": return None
    sys_req_id = prompt_input("System Req ID: ")
    if sys_req_id == "EXIT": return None
    return {"swarm_req_id": swarm_req_id, "sys_req_id": sys_req_id}

def prompt_sysreq_children():
    print("\nLink system requirement and subsystem requirement (sysreq_children table (type 'exit' to cancel)):")
    sys_req_id = prompt_input("System Req ID: ")
    if sys_req_id == "EXIT": return None
    sub_req_id = prompt_input("Subsystem Req ID: ")
    if sub_req_id == "EXIT": return None
    return {"sys_req_id": sys_req_id, "sub_req_id": sub_req_id}

def prompt_subsys_join_item():
    print("\nLink subsystem requirement and item (subsys_join_item table (type 'exit' to cancel)):")
    item_id = prompt_input("Item ID: ")
    if item_id == "EXIT": return None
    sub_req_id = prompt_input("Subsystem Req ID: ")
    if sub_req_id == "EXIT": return None
    return {"item_id": item_id, "sub_req_id": sub_req_id}

def prompt_V_join_documents():
    print("\nLink test/verification and document (V_join_documents table (type 'exit' to cancel)):")
    method_id = prompt_input("Method ID: ")
    if method_id == "EXIT": return None
    doc_id = prompt_input("Document ID: ")
    if doc_id == "EXIT": return None
    return {"method_id": method_id, "doc_id": doc_id}

def prompt_quality_requirements():
    print("\nInsert quality requirement (type 'exit' to cancel):")
    quality_rec_id = prompt_input("Quality Req ID (leave blank for auto): ", optional=True)
    if quality_rec_id == "EXIT": return None
    requirement = prompt_input("Requirement description: ")
    if requirement == "EXIT": return None
    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H): ")
    if author == "EXIT": return None
    approved_by = prompt_input("Approved by (Y.M.B or empty): ", optional=True)
    if approved_by == "EXIT": return None
    return {"quality_rec_id": quality_rec_id, "requirement": requirement, "author": author, "approved_by": approved_by}

def prompt_id_glossary():
    print("\nInsert glossary entry (type 'exit' to cancel):")
    prefix = prompt_input("Prefix: ")
    if prefix == "EXIT": return None
    meaning = prompt_input("Meaning: ")
    if meaning == "EXIT": return None
    return {"prefix": prefix, "meaning": meaning}

def prompt_item():
    print("\nInsert Item (type 'exit' to cancel)")
    item_id = prompt_input("Item ID (leave blank for auto): ", optional=True)
    if item_id == "EXIT":
        return None
    item_name = prompt_input("Item Name: ")
    if item_name == "EXIT":
        return None
    return {"item_id": item_id, "item_name": item_name}

def prompt_document():
    print("\nInsert Document (type 'exit' to cancel)")
    doc_id = prompt_input("Document ID (leave blank for auto): ", optional=True)
    if doc_id == "EXIT":
        return None
    title = prompt_input("Title: ")
    if title == "EXIT":
        return None
    description = prompt_input("Description: ")
    if description == "EXIT":
        return None
    version_raw = prompt_input("Version (optional integer): ", optional=True)
    if version_raw == "EXIT":
        return None
    version = int(version_raw) if (isinstance(version_raw, str) and version_raw.isdigit()) else None
    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H, optional): ", optional=True)
    if author == "EXIT":
        return None
    # file path omitted -> None
    return {
        "doc_id": doc_id,
        "title": title,
        "description": description,
        "file": None,
        "version": version,
        "author": author or None
    }

def prompt_vv_method():
    print("\nInsert V&V Method (type 'exit' to cancel)")
    method_id = prompt_input("Method ID (leave blank for auto): ", optional=True)
    if method_id == "EXIT":
        return None
    description = prompt_input("Description: ")
    if description == "EXIT":
        return None
    method_type = prompt_input("Method Type (Inspection/Analysis/Test): ")
    if method_type == "EXIT":
        return None
    return {"method_id": method_id, "description": description, "method_type": method_type}

# ----- OTHER PROMPTS -----
def prompt_update_row():
    print("\n================  UPDATE  ================")
    print("Update database row (type 'exit' to cancel):")

    # Read DB name (centralized)
    db_name = DB_NAME_TXT.read_text().strip()

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # 1️⃣ List all available tables in the database
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cur.fetchall() if row[0] != "sqlite_sequence"]
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return None

    print("\nSelect table to update:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}: {table}")

    table_choice = input("Enter number corresponding to the table: ").strip()
    if not table_choice.isdigit() or not (1 <= int(table_choice) <= len(tables)):
        print("Invalid choice. Returning to menu.")
        conn.close()
        return None

    table = tables[int(table_choice) - 1]

    # 2️⃣ Identify the ID column (first one ending in "_id" or containing "id")
    cur.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cur.fetchall()]
    id_column = next((c for c in columns if c.endswith("_id") or c.lower() == "id"), None)

    if not id_column:
        print(f"No obvious ID column found for table '{table}'.")
        print("You’ll need to specify one manually.")
        id_column = input("Enter the column name that uniquely identifies rows: ").strip()

    print(f"\nYou selected '{table}'. Identifying rows by '{id_column}'.")

    # 3️⃣ Ask for ID value and verify existence
    condition_value = prompt_input(f"Enter the {id_column} of the row to update: ")
    if condition_value == "EXIT":
        conn.close()
        return None

    cur.execute(f"SELECT * FROM {table} WHERE {id_column} = ? LIMIT 1", (condition_value,))
    row = cur.fetchone()
    if not row:
        print(f"No row found in '{table}' with {id_column} = '{condition_value}'.")
        conn.close()
        return None

    # Show current full row
    print("\nCurrent row data:")
    for col, val in zip(columns, row):
        print(f"  {col}: {val}")

    # 4️⃣ Let user pick column to update
    updatable_columns = [c for c in columns if c != id_column]
    print("\nSelect the column to update:")
    for i, col in enumerate(updatable_columns, start=1):
        print(f"{i}: {col}")

    col_choice = input("Enter number corresponding to the column: ").strip()
    if not col_choice.isdigit() or not (1 <= int(col_choice) <= len(updatable_columns)):
        print("Invalid choice. Returning to menu.")
        conn.close()
        return None

    update_column = updatable_columns[int(col_choice) - 1]

    # Show current value
    cur.execute(
        f"SELECT {update_column} FROM {table} WHERE {id_column} = ? LIMIT 1",
        (condition_value,)
    )
    current_value = cur.fetchone()
    shown_value = "(NULL)" if not current_value or current_value[0] is None else str(current_value[0])
    print(f"\nCurrent value of '{update_column}': {shown_value}")

    # 5️⃣ Ask for new value
    new_value = prompt_input(f"Enter the new value for '{update_column}': ")
    if new_value == "EXIT":
        conn.close()
        return None

    conn.close()

    # 6️⃣ Return update parameters
    return {
        "table": table,
        "condition_column": id_column,
        "condition_value": condition_value,
        "update_column": update_column,
        "new_value": new_value
    }

def prompt_delete_row():
    print("\nDelete database row (type 'exit' to cancel):")

    db_name = DB_NAME_TXT.read_text().strip()

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cur.fetchall() if row[0] != "sqlite_sequence"]
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return None

    print("\nSelect table to delete from:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}: {table}")

    table_choice = input("Enter number corresponding to the table: ").strip()
    if not table_choice.isdigit() or not (1 <= int(table_choice) <= len(tables)):
        print("Invalid choice. Returning to menu.")
        conn.close()
        return None

    table = tables[int(table_choice) - 1]

    # find likely ID column
    cur.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cur.fetchall()]
    id_column = next((c for c in columns if c.endswith("_id") or c.lower() == "id"), None)
    if not id_column:
        print(f"No obvious ID column found for table '{table}'.")
        id_column = input("Enter the column name that uniquely identifies rows: ").strip()

    print(f"\nYou selected '{table}'. Deleting by '{id_column}'.")
    condition_value = prompt_input(f"Enter the {id_column} of the row to DELETE: ")
    if condition_value == "EXIT":
        conn.close()
        return None

    # show the row that would be deleted (if exists)
    cur.execute(f"SELECT * FROM {table} WHERE {id_column} = ? LIMIT 1", (condition_value,))
    row = cur.fetchone()
    if not row:
        print(f"No row found in '{table}' with {id_column} = '{condition_value}'.")
        conn.close()
        return None

    print("\nRow to be deleted:")
    for col, val in zip(columns, row):
        print(f"  {col}: {val}")

    confirm = input("Are you sure you want to delete this row? (y/N): ").strip().lower()
    conn.close()
    if confirm != "y":
        print("Deletion cancelled.")
        return None

    return {
        "table": table,
        "condition_column": id_column,
        "condition_value": condition_value
    }
