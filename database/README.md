# How to run the Database

## Admin
*AKA: Running the database for the **absolute** first time*
*AKA: You don't have the file "IRDS_requirements.db"*

1. Open the branch "feature/database" in VSCode
2. Open a New Terminal
3. cd database
4. python setup_database.py
5. *Follow prompts*
6. Ensure IRDS_requirements.db gets created
7. Push your local changes to the branch
8. Done

## User
*AKA: You want to enter requirements into the database*
Pre-requisites: VSCode with SQLite3 Extension

1. Create a branch from feature/database (example: feature/database-VVM)
2. Open your branch in VSCode
3. Open a New Terminal
4. cd database
5. python run_database.py
6. *Follow prompts*
