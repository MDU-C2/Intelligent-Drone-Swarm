# menu_actions.py
"""
Handlers for TUI actions to keep run_database.py uncluttered.
Each handler prints its own success/error messages.
"""

from ..dataman.export_tools import export_db_to_json_interactive, export_db_to_csv_interactive
from ..dataman.safe_restore import safe_restore_from_json
from ..app.verify_roundtrip import run_roundtrip_check
import database.viz.plot_tree as plot_tree
import database.tui.prompts as prompts
from ..tui.delete_preview import preview_delete, print_preview, perform_delete
from database.core.paths import DB_NAME_TXT, JSON_DUMP, CSV_DIR
from pathlib import Path

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

def handle_export_json():
    db_path = DB_NAME_TXT.read_text().strip()
    export_db_to_json_interactive(db_path)

def handle_export_csv():
    export_db_to_csv_interactive()

def handle_restore_json() -> dict:
    current_db = DB_NAME_TXT.read_text().strip()
    # if you’ve locked paths, you can skip prompts entirely; otherwise keep them:
    in_path = input("\nInput JSON path [database/data/database_dump.json]: ").strip() or str(JSON_DUMP)
    target_db = input(f"Output DB path [{Path(current_db).name}]: ").strip() or current_db
    overwrite = (input(f"Overwrite '{target_db}' if exists? (y/N): ").strip().lower() == "y")
    return safe_restore_from_json(current_db, in_path, target_db, overwrite) # type: ignore

def handle_verify_roundtrip():
    print("\n→ Running round-trip verification (dump → restore → compare)…")
    try:
        run_roundtrip_check()
        print("JSON round-trip test PASSED")
    except SystemExit as se:
        print(f"Round-trip test FAILED: {se}")
    except Exception as e:
        print(f"Round-trip test error: {e}")

def handle_delete_with_preview():
    print("\nDelete with preview:")
    print("Select entity type:")
    print("  1) Goal                (goals.goal_id)")
    print("  2) Swarm requirement   (drone_swarm_requirements.swarm_req_id)")
    print("  3) System requirement  (system_requirements.sys_req_id)")
    print("  4) Subsystem req       (subsystem_requirements.sub_req_id)")
    print("  5) V&V method          (test_and_verification.method_id)")
    print("  6) Document            (documents.doc_id)")
    print("  7) Item                (item.item_id)")
    print("  8) Quality requirement (quality_requirements.quality_rec_id)")
    choice = input("Enter 1-8: ").strip()

    mapping = {
        "1": ("goal", "Goal ID"),
        "2": ("swarm", "Swarm Req ID"),
        "3": ("system", "System Req ID"),
        "4": ("subsystem", "Sub Req ID"),
        "5": ("method", "Method ID"),
        "6": ("document", "Doc ID"),
        "7": ("item", "Item ID"),
        "8": ("quality", "Quality Req ID"),
    }
    if choice not in mapping:
        print("Invalid choice.")
        return

    entity_type, label = mapping[choice]
    entity_id = input(f"Enter {label}: ").strip()
    if not entity_id:
        print("Cancelled.")
        return

    try:
        p = preview_delete(entity_type, entity_id)
        print_preview(p)
        confirm = input(f"\nType the exact ID ({entity_id}) to CONFIRM delete, or press ENTER to cancel: ").strip()
        if confirm != entity_id:
            print("Cancelled.")
            return
        deleted = perform_delete(p)
        if deleted == 1:
            print("Deleted. (Linked rows removed via CASCADE, children detached via SET NULL.)")
        else:
            print("Nothing deleted (ID not found).")
    except Exception as e:
        print(f"Delete failed: {e}")

def handle_show_restore_instructions():
    db_path = Path(DB_NAME_TXT.read_text().strip())
    db_file = db_path.name
    print(rf"""
================  Restore JSON → DB  ================

1) Choose **23: Exit** to close the database.

2) In the Terminal, run:
   python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/{db_file} --overwrite

3) Start the app again:
   python -m database.app.run_database
=======================================================================
""")
