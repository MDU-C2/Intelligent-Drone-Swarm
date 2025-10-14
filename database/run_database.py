# run_database.py

from connect_database import connect_database
from insert_functions import insert_functions
import plot_tree
import prompts
from db_utilities import db_utilities
from db_json_bridge import dump_db_to_json, restore_db_from_json
from verify_roundtrip import run_roundtrip_check
from export_db_to_csv import export_db_to_csv

# MENU CHOICE CONSTANTS
INSERT_GOAL = "1"
INSERT_DRONE_SWARM_REQ = "2"
INSERT_SYS_REQ = "3"
INSERT_SUBSYS_REQ = "4"
INSERT_ITEM = "5"
INSERT_DOCUMENT = "6"
INSERT_VV_METHOD = "7"
INSERT_QUALITY_REQ = "8"
INSERT_GOAL_CHILDREN = "9"
INSERT_SWARM_REQ_CHILDREN = "10"
INSERT_SYSREQ_CHILDREN = "11"
INSERT_SUBSYS_JOIN_ITEM = "12"
INSERT_V_JOIN_DOCS = "13"
INSERT_ID_GLOSSARY = "14"
PLOT_TREE = "15"
SEARCH_DB = "16"
UPDATE_DB_ROW = "17"
DELETE_DB_ROW = "18"
EXPORT_TO_JSON = "19"
RESTORE_FROM_JSON = "20"
VERIFY_ROUNDTRIP = "21"
EXPORT_TO_CSV = "22"
EXIT = "23"

def wait_for_enter():
    input("\nPress ENTER to return to the menu...")

def main():
    with open("db_name.txt", "r") as f:
        db_name = f.read().strip()
        
    with connect_database(db_name) as db:
        inserter = insert_functions(db.cursor)
        other = db_utilities(db.cursor)

        while True:
            print("\nSelect action:")
            print("1: Insert a Goal")
            print("2: Insert a Drone Swarm Requirement")
            print("3: Insert a System Requirement")
            print("4: Insert a Subsystem Requirement")
            print("5: Insert an Item")
            print("6: Insert a Document")
            print("7: Insert a V&V Method")
            print("8: Insert Quality Requirement")
            print("9: Connect Drone Swarm Requirement to Goal")
            print("10: Connect System Requirement to Drone Swarm Requirement")
            print("11: Connect System Requiement to Subsystem Requirement")
            print("12: Connect Item to Subsystem Requirement")
            print("13: Connect Document to V&V Method")
            print("14: Add ID to Glossary")
            print("15: Plot tree")
            print("16: Search in Database")
            print("17: Update row in Database")
            print("18: Delete row in Database")
            print("19: Export DB → JSON")
            print("20: Restore JSON → DB")
            print("21: Verify JSON round-trip")
            print("22: Export DB → CSV")  # ⬅️ NEW
            print("23: Exit")             # ⬅️ shifted

            choice = input("Enter choice (1-23): ")

            try:
                if choice == INSERT_GOAL:
                    data = prompts.prompt_goal()
                    if data:
                        inserter.insert_goal(**data)
                        print("Goal inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_DRONE_SWARM_REQ:
                    data = prompts.prompt_drone_swarm_requirement()
                    if data:
                        inserter.insert_drone_swarm_requirements(**data)
                        print("Drone Swarm Requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_SYS_REQ:
                    data = prompts.prompt_system_requirement()
                    if data:
                        inserter.insert_system_requirements(**data)
                        print("System Requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_SUBSYS_REQ:
                    data = prompts.prompt_subsystem_requirement()
                    if data:
                        inserter.insert_subsystem_requirements(**data)
                        print("Subsystem Requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_ITEM:
                    data = prompts.prompt_item()
                    if data:
                        inserter.insert_item(**data)
                        print("Item inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_DOCUMENT:
                    data = prompts.prompt_document()
                    if data:
                        inserter.insert_documents(**data)
                        print("Document inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_VV_METHOD:
                    data = prompts.prompt_vv_method()
                    if data:
                        inserter.insert_test_and_verification(**data)
                        print("V&V Method inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_QUALITY_REQ:
                    data = prompts.prompt_quality_requirements()
                    if data:
                        inserter.insert_quality_requirements(**data)
                        print("Quality requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == INSERT_GOAL_CHILDREN:
                    data = prompts.prompt_goal_children()
                    if data:
                        inserter.insert_goal_children(**data)
                        print("Successfully connected Drone Swarm Requirement to Goal!")
                    else:
                        print("Connection cancelled.")
                    wait_for_enter()

                elif choice == INSERT_SWARM_REQ_CHILDREN:
                    data = prompts.prompt_swarm_req_children()
                    if data:
                        inserter.insert_swarm_req_children(**data)
                        print("Successfully connected System Requirement to Drone Swarm Requirement!")
                    else:
                        print("Connection cancelled.")
                    wait_for_enter()

                elif choice == INSERT_SYSREQ_CHILDREN:
                    data = prompts.prompt_sysreq_children()
                    if data:
                        inserter.insert_sysreq_children(**data)
                        print("Successfully connected System Requirement to Subsystem Requirement!")
                    else:
                        print("Connection cancelled.")
                    wait_for_enter()

                elif choice == INSERT_SUBSYS_JOIN_ITEM:
                    data = prompts.prompt_subsys_join_item()
                    if data:
                        inserter.insert_subsys_join_item(**data)
                        print("Successfully connected Item to Subsystem Requirement!")
                    else:
                        print("Connection cancelled.")
                    wait_for_enter()

                elif choice == INSERT_V_JOIN_DOCS:
                    data = prompts.prompt_V_join_documents()
                    if data:
                        inserter.insert_V_join_documents(**data)
                        print("Successfully connected Document to V&V Method!")
                    else:
                        print("Connection cancelled.")
                    wait_for_enter()

                elif choice == INSERT_ID_GLOSSARY:
                    data = prompts.prompt_id_glossary()
                    if data:
                        inserter.insert_id_glossary(**data)
                        print("ID successfully inserted to ID Glossary!")
                    else:
                        print("Insertion cancelled.")
                    wait_for_enter()

                elif choice == PLOT_TREE:
                    try:
                        plot_tree.run_tree_plot()
                    except Exception as e:
                        print(f"Error plotting tree: {e}")

                elif choice == SEARCH_DB:
                    other.interactive_search()
                    wait_for_enter()

                elif choice == UPDATE_DB_ROW:
                    data = prompts.prompt_update_row()
                    if data:
                        affected = other.update_row(**data)
                        print("Row updated successfully!" if affected else "No rows matched your criteria.")
                    else:
                        print("Update cancelled.")
                    wait_for_enter()

                elif choice == DELETE_DB_ROW:
                    data = prompts.prompt_delete_row()
                    if data:
                        affected = other.delete_from_table(
                            data["table"], data["condition_column"], data["condition_value"]
                        )
                        print("Row deleted successfully!" if affected else "No rows matched your criteria.")
                    else:
                        print("Deletion cancelled.")
                    wait_for_enter()
                
                elif choice == EXPORT_TO_JSON:
                    default_json = "database_dump.json"
                    out_path = input(f"\nOutput JSON path [{default_json}]: ").strip() or default_json
                    try:
                        dump_db_to_json(db_name, out_path)
                        print(f"Exported '{db_name}' → '{out_path}'")
                    except Exception as e:
                        print(f"Export failed: {e}")
                    wait_for_enter()

                elif choice == RESTORE_FROM_JSON:
                    in_path = input("\nInput JSON path [database_dump.json]: ").strip() or "database_dump.json"
                    target_db = input(f"Output DB path [{db_name}]: ").strip() or db_name
                    overwrite = (input(f"Overwrite '{target_db}' if exists? (y/N): ").strip().lower() == "y")
                    try:
                        restore_db_from_json(target_db, in_path, overwrite=overwrite)
                        print(f"Restored '{target_db}' from '{in_path}' (overwrite={overwrite})")
                    except Exception as e:
                        print(f"Restore failed: {e}")
                    wait_for_enter()

                elif choice == VERIFY_ROUNDTRIP:
                    print("\n→ Running round-trip verification (dump → restore → compare)…")
                    try:
                        run_roundtrip_check()
                        print("JSON round-trip test PASSED")
                    except SystemExit as se:
                        print(f"Round-trip test FAILED: {se}")
                    except Exception as e:
                        print(f"Round-trip test error: {e}")
                    wait_for_enter()

                elif choice == EXPORT_TO_CSV:
                    out_dir_default = "csv_exports"
                    out_dir = input(f"\nOutput folder for CSVs [{out_dir_default}]: ").strip() or out_dir_default
                    try:
                        export_db_to_csv(out_dir)
                    except Exception as e:
                        print(f"CSV export failed: {e}")
                    wait_for_enter()

                elif choice == EXIT:
                    print("Exiting script.")
                    break

                else:
                    print("Invalid choice. Try again.")

            except Exception as e:
                print(f"Error inserting data: {e}")

if __name__ == "__main__":
    main()
