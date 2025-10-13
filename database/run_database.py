# run_database.py

from connect_database import connect_database
from insert_functions import insert_functions
import plot_tree
import prompts
from db_utilities import db_utilities

# ----- MENU CHOICE CONSTANTS -----
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
EXIT = "18"

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
            print("11: Connect System Requiement to System or Subsystem Requirement")
            print("12: Connect Item to Subsystem Requirement")
            print("13: Connect Document to V&V Method")
            print("14: Add ID to Glossary")
            print("15: Plot tree")
            print("16: Search in Database")
            print("17: Update row in Database")
            print("18: Exit")

            choice = input("Enter choice (1-18): ")

            try:
                if choice == INSERT_GOAL:
                    data = prompts.prompt_goal()
                    if data:
                        inserter.insert_goal(**data)
                        print("Goal inserted successfully!")
                    else:
                        print("Insertion cancelled.")

                elif choice == INSERT_DRONE_SWARM_REQ:
                    data = prompts.prompt_drone_swarm_requirement()
                    if data:
                        inserter.insert_drone_swarm_requirements(**data)
                        print("Drone Swarm Requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")

                elif choice == INSERT_SYS_REQ:
                    data = prompts.prompt_system_requirement()
                    if data:
                        inserter.insert_system_requirements(**data)
                        print("System Requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")

                elif choice == INSERT_SUBSYS_REQ:
                    data = prompts.prompt_subsystem_requirement()
                    if data:
                        inserter.insert_subsystem_requirements(**data)
                        print("Subsystem Requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")


                elif choice == INSERT_ITEM:
                    print("\nInsert Item (type 'exit' to cancel)")
                    item_id = input("Item ID: ").strip()
                    if item_id.lower() == "exit": 
                        print("Insertion cancelled.")
                    else:
                        item_name = input("Item Name: ").strip()
                        if item_name.lower() == "exit":
                            print("Insertion cancelled.")
                        else:
                            inserter.insert_item(item_id, item_name)
                            print("Item inserted successfully!")

                elif choice == INSERT_DOCUMENT:
                    print("\nInsert Document (type 'exit' to cancel)")
                    doc_id = input("Doc ID: ").strip()
                    if doc_id.lower() == "exit":
                        print("Insertion cancelled.")
                    else:
                        title = input("Title: ").strip()
                        description = input("Description: ").strip()
                        version_raw = input("Version (optional integer): ").strip()
                        version = int(version_raw) if version_raw.isdigit() else None
                        author = input("Author (E.Z/C.N/Y.M.B/E.M/A.H, optional): ").strip() or None
                        # Binary file path skipped for now; store as NULL
                        inserter.insert_documents(doc_id, title, description, None, version, author)
                        print("Document inserted successfully!")

                elif choice == INSERT_VV_METHOD:
                    print("\nInsert V&V Method (type 'exit' to cancel)")
                    method_id = input("Method ID: ").strip()
                    if method_id.lower() == "exit":
                        print("Insertion cancelled.")
                    else:
                        description = input("Description: ").strip()
                        method_type = input("Method Type (Inspection/Analysis/Test): ").strip()
                        inserter.insert_test_and_verification(method_id, description, method_type)
                        print("V&V Method inserted successfully!")

                elif choice == INSERT_QUALITY_REQ:
                    data = prompts.prompt_quality_requirements()
                    if data:
                        inserter.insert_quality_requirements(**data)
                        print("Quality requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")


                elif choice == INSERT_GOAL_CHILDREN:
                    data = prompts.prompt_goal_children()
                    if data:
                        inserter.insert_goal_children(**data)
                        print("Successfully connected Drone Swarm Requirement to Goal!")
                    else:
                        print("Connection cancelled.")

                elif choice == INSERT_SWARM_REQ_CHILDREN:
                    data = prompts.prompt_swarm_req_children()
                    if data:
                        inserter.insert_swarm_req_children(**data)
                        print("Successfully connected System Requirement to Drone Swarm Requirement!")
                    else:
                        print("Connection cancelled.")

                elif choice == INSERT_SYSREQ_CHILDREN:
                    data = prompts.prompt_sysreq_children()
                    if data:
                        inserter.insert_sysreq_children(**data)
                        print("Successfully connected System Requirement to System/Subsystem Requirement!")
                    else:
                        print("Connection cancelled.")

                elif choice == INSERT_SUBSYS_JOIN_ITEM:
                    data = prompts.prompt_subsys_join_item()
                    if data:
                        inserter.insert_subsys_join_item(**data)
                        print("Successfully connected Item to Subsystem Requirement!")
                    else:
                        print("Connection cancelled.")

                elif choice == INSERT_V_JOIN_DOCS:
                    data = prompts.prompt_V_join_documents()
                    if data:
                        inserter.insert_V_join_documents(**data)
                        print("Successfully connected Document to V&V Method!")
                    else:
                        print("Connection cancelled.")

                elif choice == INSERT_QUALITY_REQ:
                    data = prompts.prompt_quality_requirements()
                    if data:
                        inserter.insert_quality_requirements(**data)
                        print("Quality requirement inserted successfully!")
                    else:
                        print("Insertion cancelled.")

                elif choice == INSERT_ID_GLOSSARY:
                    data = prompts.prompt_id_glossary()
                    if data:
                        inserter.insert_id_glossary(**data)
                        print("ID successfully inserted to ID Glossary!")
                    else:
                        print("Insertion cancelled.")

                elif choice == PLOT_TREE:
                    try:
                        plot_tree.run_tree_plot()
                    except Exception as e:
                        print(f"Error plotting tree: {e}")

                elif choice == SEARCH_DB:
                    try:
                        tables = other.list_tables()
                        if not tables:
                            print("No tables found in the database.")
                            continue

                        print("\nAvailable tables:")
                        for i, t in enumerate(tables, start=1):
                            print(f"{i}: {t}")

                        table_choice = input("Select table by number: ").strip()
                        if not table_choice.isdigit() or not (1 <= int(table_choice) <= len(tables)):
                            print("Invalid table choice.")
                            continue
                        table = tables[int(table_choice) - 1]

                        columns = other.list_columns(table)
                        if not columns:
                            print("No columns found for this table.")
                            continue

                        print("\nAvailable columns:")
                        for i, c in enumerate(columns, start=1):
                            print(f"{i}: {c}")

                        column_choice = input("Select column by number: ").strip()
                        if not column_choice.isdigit() or not (1 <= int(column_choice) <= len(columns)):
                            print("Invalid column choice.")
                            continue
                        column = columns[int(column_choice) - 1]

                        value = input(f"Enter value to search in '{column}': ").strip()
                        partial = input("Partial match? (y/n): ").strip().lower() == "y"

                        rows = other.search_value(table, column, value, partial=partial)
                        if rows:
                            print(f"\nFound {len(rows)} matching row(s):")
                            other.pretty_print_rows(table, rows)
                        else:
                            print("No matches found.")

                    except Exception as e:
                        print(f"Error searching database: {e}")

                elif choice == UPDATE_DB_ROW:
                        data = prompts.prompt_update_row()
                        if data:
                            affected = other.update_row(**data)
                            print("Row updated successfully!" if affected else "No rows matched your criteria.")
                        else:
                            print("Update cancelled.")
                    
                elif choice == EXIT:
                    print("Exiting script.")
                    break

                else:
                    print("Invalid choice. Try again.")

            except Exception as e:
                print(f"Error inserting data: {e}")

if __name__ == "__main__":
    main()
