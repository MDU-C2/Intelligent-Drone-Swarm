# menu_actions.py
"""
Handlers for TUI actions to keep run_database.py uncluttered.
Each handler prints its own success/error messages.
"""

from export_tools import export_db_to_json_interactive, export_db_to_csv_interactive
from safe_restore import safe_restore_from_json
from verify_roundtrip import run_roundtrip_check
import plot_tree
import prompts

def handle_insert_goal(inserter):
    data = prompts.prompt_goal()
    if data:
        inserter.insert_goal(**data)
        print("Goal inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_drone_swarm(inserter):
    data = prompts.prompt_drone_swarm_requirement()
    if data:
        inserter.insert_drone_swarm_requirements(**data)
        print("Drone Swarm Requirement inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_system(inserter):
    data = prompts.prompt_system_requirement()
    if data:
        inserter.insert_system_requirements(**data)
        print("System Requirement inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_subsystem(inserter):
    data = prompts.prompt_subsystem_requirement()
    if data:
        inserter.insert_subsystem_requirements(**data)
        print("Subsystem Requirement inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_item(inserter):
    data = prompts.prompt_item()
    if data:
        inserter.insert_item(**data)
        print("Item inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_document(inserter):
    data = prompts.prompt_document()
    if data:
        inserter.insert_documents(**data)
        print("Document inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_vv_method(inserter):
    data = prompts.prompt_vv_method()
    if data:
        inserter.insert_test_and_verification(**data)
        print("V&V Method inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_insert_quality_requirement(inserter):
    data = prompts.prompt_quality_requirements()
    if data:
        inserter.insert_quality_requirements(**data)
        print("Quality requirement inserted successfully!")
    else:
        print("Insertion cancelled.")

def handle_goal_children(inserter):
    data = prompts.prompt_goal_children()
    if data:
        inserter.insert_goal_children(**data)
        print("Successfully connected Drone Swarm Requirement to Goal!")
    else:
        print("Connection cancelled.")

def handle_swarm_req_children(inserter):
    data = prompts.prompt_swarm_req_children()
    if data:
        inserter.insert_swarm_req_children(**data)
        print("Successfully connected System Requirement to Drone Swarm Requirement!")
    else:
        print("Connection cancelled.")

def handle_sysreq_children(inserter):
    data = prompts.prompt_sysreq_children()
    if data:
        inserter.insert_sysreq_children(**data)
        print("Successfully connected System Requirement to Subsystem Requirement!")
    else:
        print("Connection cancelled.")

def handle_subsys_join_item(inserter):
    data = prompts.prompt_subsys_join_item()
    if data:
        inserter.insert_subsys_join_item(**data)
        print("Successfully connected Item to Subsystem Requirement!")
    else:
        print("Connection cancelled.")

def handle_v_join_documents(inserter):
    data = prompts.prompt_V_join_documents()
    if data:
        inserter.insert_V_join_documents(**data)
        print("Successfully connected Document to V&V Method!")
    else:
        print("Connection cancelled.")

def handle_id_glossary(inserter):
    data = prompts.prompt_id_glossary()
    if data:
        inserter.insert_id_glossary(**data)
        print("ID successfully inserted to ID Glossary!")
    else:
        print("Insertion cancelled.")

def handle_plot_tree():
    try:
        plot_tree.run_tree_plot()
    except Exception as e:
        print(f"Error plotting tree: {e}")

def handle_search(other):
    other.interactive_search()

def handle_update(other):
    data = prompts.prompt_update_row()
    if data:
        affected = other.update_row(**data)
        print("Row updated successfully!" if affected else "No rows matched your criteria.")
    else:
        print("Update cancelled.")

def handle_delete(other):
    data = prompts.prompt_delete_row()
    if data:
        affected = other.delete_from_table(
            data["table"], data["condition_column"], data["condition_value"]
        )
        print("Row deleted successfully!" if affected else "No rows matched your criteria.")
    else:
        print("Deletion cancelled.")

def handle_export_json(db_name: str):
    export_db_to_json_interactive(db_name)

def handle_export_csv():
    export_db_to_csv_interactive()

def handle_restore_json(db_name: str) -> str:
    in_path = input("\nInput JSON path [database_dump.json]: ").strip() or "database_dump.json"
    target_db = input(f"Output DB path [{db_name}]: ").strip() or db_name
    overwrite = (input(f"Overwrite '{target_db}' if exists? (y/N): ").strip().lower() == "y")
    result = safe_restore_from_json(db_name, in_path, target_db, overwrite)
    return result  # "exit" or "continue"

def handle_verify_roundtrip():
    print("\n→ Running round-trip verification (dump → restore → compare)…")
    try:
        run_roundtrip_check()
        print("JSON round-trip test PASSED")
    except SystemExit as se:
        print(f"Round-trip test FAILED: {se}")
    except Exception as e:
        print(f"Round-trip test error: {e}")
