# run_database.py

from connect_database import connect_database
from insert_functions import insert_functions
from db_utilities import db_utilities

from menu_actions import (
    handle_insert_goal,
    handle_insert_drone_swarm,
    handle_insert_system,
    handle_insert_subsystem,
    handle_insert_item,
    handle_insert_document,
    handle_insert_vv_method,
    handle_insert_quality_requirement,
    handle_goal_children,
    handle_swarm_req_children,
    handle_sysreq_children,
    handle_subsys_join_item,
    handle_v_join_documents,
    handle_id_glossary,
    handle_plot_tree,
    handle_search,
    handle_update,
    handle_delete,
    handle_export_json,
    handle_export_csv,
    handle_restore_json,
    handle_verify_roundtrip,
    handle_delete_with_preview,
)

from tui_helpers import wait_for_enter

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

def main():
    with open("db_name.txt", "r") as f:
        db_name = f.read().strip()

    with connect_database(db_name) as db:
        inserter = insert_functions(db.cursor)
        other = db_utilities(db.cursor)

        while True:
            print("\nSelect action:")
            print("1:  Insert a Goal")
            print("2:  Insert a Drone Swarm Requirement")
            print("3:  Insert a System Requirement")
            print("4:  Insert a Subsystem Requirement")
            print("5:  Insert an Item")
            print("6:  Insert a Document")
            print("7:  Insert a V&V Method")
            print("8:  Insert Quality Requirement")
            print("9:  Connect Drone Swarm Requirement to Goal")
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
            print("22: Export DB → CSV")
            print("23: Exit")

            choice = input("Enter choice (1-23): ").strip()

            try:
                if choice == INSERT_GOAL:
                    handle_insert_goal(inserter)

                elif choice == INSERT_DRONE_SWARM_REQ:
                    handle_insert_drone_swarm(inserter)

                elif choice == INSERT_SYS_REQ:
                    handle_insert_system(inserter)

                elif choice == INSERT_SUBSYS_REQ:
                    handle_insert_subsystem(inserter)

                elif choice == INSERT_ITEM:
                    handle_insert_item(inserter)

                elif choice == INSERT_DOCUMENT:
                    handle_insert_document(inserter)

                elif choice == INSERT_VV_METHOD:
                    handle_insert_vv_method(inserter)

                elif choice == INSERT_QUALITY_REQ:
                    handle_insert_quality_requirement(inserter)

                elif choice == INSERT_GOAL_CHILDREN:
                    handle_goal_children(inserter)

                elif choice == INSERT_SWARM_REQ_CHILDREN:
                    handle_swarm_req_children(inserter)

                elif choice == INSERT_SYSREQ_CHILDREN:
                    handle_sysreq_children(inserter)

                elif choice == INSERT_SUBSYS_JOIN_ITEM:
                    handle_subsys_join_item(inserter)

                elif choice == INSERT_V_JOIN_DOCS:
                    handle_v_join_documents(inserter)

                elif choice == INSERT_ID_GLOSSARY:
                    handle_id_glossary(inserter)

                elif choice == PLOT_TREE:
                    handle_plot_tree()

                elif choice == SEARCH_DB:
                    handle_search(other)

                elif choice == UPDATE_DB_ROW:
                    handle_update(other)

                elif choice == DELETE_DB_ROW:
                    #handle_delete(other)
                    handle_delete_with_preview()

                elif choice == EXPORT_TO_JSON:
                    handle_export_json(db_name)

                elif choice == RESTORE_FROM_JSON:
                    result = handle_restore_json(db_name)
                    if result == "exit":
                        break

                elif choice == VERIFY_ROUNDTRIP:
                    handle_verify_roundtrip()

                elif choice == EXPORT_TO_CSV:
                    handle_export_csv()

                elif choice == EXIT:
                    print("Exiting script.")
                    break

                else:
                    print("Invalid choice. Try again.")

            except Exception as e:
                print(f"Error: {e}")

            # Pause before showing the menu again
            wait_for_enter()

if __name__ == "__main__":
    main()
