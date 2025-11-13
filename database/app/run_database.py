# run_database.py

from database.core.paths import DB_NAME_TXT
from ..core.connect_database import connect_database
from ..core.insert_functions import insert_functions
from ..core.db_utilities import db_utilities
import database.tui.menu_actions as menu
from ..tui.tui_helpers import wait_for_enter

# MENU CHOICE CONSTANTS
INSERT_GOAL = "1"
INSERT_DRONE_SWARM_REQ = "2"
INSERT_SYS_REQ = "3"
INSERT_SUBSYS_REQ = "4"
INSERT_DOCUMENT = "5"
INSERT_VV_METHOD = "6"
INSERT_QUALITY_REQ = "7"
INSERT_GOAL_CHILDREN = "8"
INSERT_SWARM_REQ_CHILDREN = "9"
INSERT_SYSREQ_CHILDREN = "10"
INSERT_V_JOIN_DOCS = "11"
DELETE_TABLE = "12"
INSERT_ID_GLOSSARY = "13"
PLOT_TREE = "14"
SEARCH_DB = "15"
UPDATE_DB_ROW = "16"
DELETE_DB_ROW = "17"
EXPORT_TO_JSON = "18"
RESTORE_FROM_JSON = "19"
EXPORT_TO_CSV = "20"
EXPORT_DOC = "21"
EXIT = "22"

VERIFY_ROUNDTRIP = "23"

def main():
    db_name = DB_NAME_TXT.read_text().strip()

    with connect_database(db_name) as db:
        # Pass both cursor and connection so ID generation can serialize writers.
        inserter = insert_functions(db.cursor, db.conn)
        other = db_utilities(db.cursor)

        while True:
            print("\n================  Select action  ================")
            print("1:  Insert a Goal")
            print("2:  Insert a Drone Swarm Requirement")
            print("3:  Insert a System Requirement")
            print("4:  Insert a Subsystem Requirement")
            print("5:  Insert a Document")
            print("6:  Insert a V&V Method")
            print("7:  Insert Quality Requirement")
            print("8:  Connect Drone Swarm Requirement to Goal")
            print("9:  Connect System Requirement to Drone Swarm Requirement")
            print("10: Connect System Requirement to Subsystem Requirement")
            print("11: Connect Document to V&V Method")
            print("12: Delete table")
            print("13: Add ID to Glossary")
            print("14: Plot tree")
            print("15: Search in Database")
            print("16: Update row in Database")
            print("17: Delete row in Database")
            print("18: Export DB → JSON")
            print("19: How to restore JSON → DB")
            print("20: Export DB → CSV")
            print("21: Export Document File")
            print("22: Exit")

            choice = input("===  Enter choice (1-22): ").strip()

            try:
                if choice == INSERT_GOAL:
                    menu.handle_insert_goal(inserter)

                elif choice == INSERT_DRONE_SWARM_REQ:
                    menu.handle_insert_drone_swarm(inserter)

                elif choice == INSERT_SYS_REQ:
                    menu.handle_insert_system(inserter)

                elif choice == INSERT_SUBSYS_REQ:
                    menu.handle_insert_subsystem(inserter)

                elif choice == INSERT_DOCUMENT:
                    menu.handle_insert_document(inserter)

                elif choice == INSERT_VV_METHOD:
                    menu.handle_insert_vv_method(inserter)

                elif choice == INSERT_QUALITY_REQ:
                    menu.handle_insert_quality_requirement(inserter)

                elif choice == INSERT_GOAL_CHILDREN:
                    menu.handle_goal_children(inserter)

                elif choice == INSERT_SWARM_REQ_CHILDREN:
                    menu.handle_swarm_req_children(inserter)

                elif choice == INSERT_SYSREQ_CHILDREN:
                    menu.handle_sysreq_children(inserter)

                elif choice == DELETE_TABLE:
                    menu.handle_delete_table(other)

                elif choice == INSERT_V_JOIN_DOCS:
                    menu.handle_v_join_documents(inserter)

                elif choice == INSERT_ID_GLOSSARY:
                    menu.handle_id_glossary(inserter)

                elif choice == PLOT_TREE:
                    menu.handle_plot_tree()

                elif choice == SEARCH_DB:
                    menu.handle_search(other)

                elif choice == UPDATE_DB_ROW:
                    menu.handle_update(other)

                elif choice == DELETE_DB_ROW:
                    #handle_delete(other)
                    menu.handle_delete_with_preview()

                elif choice == EXPORT_TO_JSON:
                    menu.handle_export_json()

                elif choice == RESTORE_FROM_JSON:
                    menu.handle_show_restore_instructions()

                elif choice == VERIFY_ROUNDTRIP:
                    menu.handle_verify_roundtrip()

                elif choice == EXPORT_TO_CSV:
                    menu.handle_export_csv()
                
                elif choice == EXPORT_DOC:
                    menu.handle_export_document_file()


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
