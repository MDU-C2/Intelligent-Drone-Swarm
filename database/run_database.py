# run_database.py
# Usage: Other users can run in terminal "python run_database.py"
# They don’t need to create tables — just connect to your pre-existing example.db and insert records.

from connect_database import connect_database
from insert_functions import insert_functions
import plot_tree
from insert_prompts import (
    prompt_goal, prompt_drone_swarm_requirement, prompt_goal_children,
    prompt_swarm_req_children, prompt_sysreq_children, prompt_subsys_join_item,
    prompt_V_join_documents, prompt_quality_requirements, prompt_id_glossary
)

def main():
    with connect_database("example.db") as db:
        inserter = insert_functions(db.cursor)

        while True:
            print("\nSelect action:")
            print("1: Insert a goal")
            print("2: Insert a drone swarm requirement")
            print("3: Insert goal_children")
            print("4: Insert swarm_req_children")
            print("5: Insert sysreq_children")
            print("6: Insert subsys_join_item")
            print("7: Insert V_join_documents")
            print("8: Insert quality_requirements")
            print("9: Insert id_glossary")
            print("10: Plot tree")
            print("11: Exit")

            choice = input("Enter choice (1-10): ")

            try:
                if choice == "1":
                    data = prompt_goal()
                    if data: inserter.insert_goal(**data)
                    print("Goal inserted successfully!")

                elif choice == "2":
                    data = prompt_drone_swarm_requirement()
                    if data: inserter.insert_drone_swarm_requirements(**data)
                    print("Drone swarm requirement inserted successfully!")

                elif choice == "3":
                    data = prompt_goal_children()
                    if data: inserter.insert_goal_children(**data)
                    print("Goal_children record inserted successfully!")

                elif choice == "4":
                    data = prompt_swarm_req_children()
                    if data: inserter.insert_swarm_req_children(**data)
                    print("Swarm_req_children record inserted successfully!")

                elif choice == "5":
                    data = prompt_sysreq_children()
                    if data: inserter.insert_sysreq_children(**data)
                    print("Sysreq_children record inserted successfully!")

                elif choice == "6":
                    data = prompt_subsys_join_item()
                    if data: inserter.insert_subsys_join_item(**data)
                    print("Subsys_join_item record inserted successfully!")

                elif choice == "7":
                    data = prompt_V_join_documents()
                    if data: inserter.insert_V_join_documents(**data)
                    print("V_join_documents record inserted successfully!")

                elif choice == "8":
                    data = prompt_quality_requirements()
                    if data: inserter.insert_quality_requirements(**data)
                    print("Quality requirement inserted successfully!")

                elif choice == "9":
                    data = prompt_id_glossary()
                    if data: inserter.insert_id_glossary(**data)
                    print("ID glossary entry inserted successfully!")

                elif choice == "10":
                    try:
                        plot_tree.run_tree_plot()
                    except Exception as e:
                        print(f"Error plotting tree: {e}")

                elif choice == "11":
                    print("Exiting script.")
                    break

                else:
                    print("Invalid choice. Try again.")

            except Exception as e:
                print(f"Error inserting data: {e}")

if __name__ == "__main__":
    main()
