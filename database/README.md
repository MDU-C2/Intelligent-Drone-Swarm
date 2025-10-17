# Beginner‑Friendly Guide to the Database

This README walks you through setting up, using, exporting, and verifying our SQLite requirements database — even if you’ve never touched SQLite or Python before.

### NOTE
- Our actual database is IRDS_requirements.db located in the branch `feature/database`
- A graphical representation of the work flow can be seen at the bottom of this page

---

## 0) What’s in the database folder?

* **SQLite database** with tables for goals, requirements (swarm/system/subsystem), verification methods, documents, items, joins, etc.
* **JSON export/restore** so we can store changes in Git and review diffs easily.
* **Graph plotter** to visualize requirement links as a tree.

Key scripts:

* `setup_database.py` — create a new `.db` and all tables, write the DB name to `db_name.txt`.
* `run_database.py` — the interactive menu (insert/search/update/delete/export/restore/verify/plot).

---

## 1) Prerequisites

1. **Python 3.10+** installed *(not 3.13 though)*
2. **VS Code** and the **SQLite** extension

---

## 2) Start inserting data

1. Create your own branch from the branch `feature/database` (example: `feature/database-VVM`)
2. Open your branch in VS Code
3. Open a Terminal and run:
(press ENTER instead of inserting a .db name)
```bash
python -m database.app.setup_database
```
4. In the Terminal run:
```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/local.db --overwrite
```


6. Right-click on `local.db` (in the `data` folder) and choose "Open Database"
7. In the Terminal run:
```bash
python -m database.app.run_database
```
6. Follow the prompts
(Type `exit` during a prompt to cancel and return to the main menu.)
7. When you're done inserting data follow the instructions under **3) Export DB → JSON, and then push to GitHub**

### Notes while inserting data

* **Authors vs. Reviewers:** they must be different *(this is enforced in the code)*.
* **Verification status:** if not `Pending`, you must supply a verification method ID that already exists.

---

## 3) Export DB → JSON, and then push to GitHub
(still on your own branch in VS Code)
1. In the Terminal run `python -m database.app.run_database`
2. Choose **Export DB → JSON**
3. Exit
4. Commit your changes
5. Push your changes to GitHub and open a Pull Request requesting to merge your branch to `feature/database`
6. If there are no conflicts you can go ahead and squash merge. But if there are conflicts ask for help from the Chief Engineer ;)
(Note: Conflicts on `local.db` has no impact on our actual database, but conflicts on `database_dump.json` does)

**Note:** The Chief Engineer and/or the Requirements Manager are in charge of inserting `database_dump.json` to `IRDS_requirements.db` in the `feature/database` branch :)

---

## 4) Troubleshooting

**Foreign key constraint failed**

* You may have inserted a child that references a non‑existent parent. Create the parent first.

**“Author and reviewer must be different” error**

* Choose different people for `author` and `reviewer`.

**“Verification method must be provided if status is not pending”**

* Add the method first (Insert V&V Method), then reference its ID when you set a non‑Pending status.

**Restore complains about unresolved parents**

* Your JSON may contain a parent that’s missing. Fix the source DB/JSON, or insert missing parents first.

**Matplotlib window doesn’t show**

* In VS Code save figures by typing `all` when prompted (files will be written to the project folder).

---

## 5) Handy copy‑paste snippets

Set up local database (press ENTER instead of inserting a .db name)
```bash
python -m database.app.setup_database
```

Load JSON to DB
```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/local.db --overwrite
```

Run interactive menu
```bash
python -m database.app.run_database
```

---
## 6) Restoring JSON → DB
**For CE/RM eyes only**
1. Open `feature/database` in VS Code
2. Open a Terminal and run:
```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/IRDS_requirements.db --overwrite
```
3. Push changes to GitHub (`IRDS_requirements.db` should be the only change)
4. Done!

---
## 7) Other

Load demo data
```bash
python -m database.tests.populate_test_data
```
or
```bash
python -m database.tests.pop_test_data
```

Both commands load in the same data, but the first command hard codes IDs and the other command uses automatic IDs

---

## 8) File/Folder overview

```
database/
├── app/ # Scripts you run (entry points)
│ ├── run_database.py # Main interactive interface
│ ├── setup_database.py # Creates the database and tables
│ └── verify_roundtrip.py # Tests DB ↔ JSON conversion integrity
│
├── core/ # Core database logic and schema
│ ├── connect_database.py # Handles database connections
│ ├── create_tables.py # Defines tables and foreign keys
│ ├── insert_functions.py # Insert helpers for each table
│ ├── db_utilities.py # Shared database utility functions
│ └── paths.py # Paths used
│
├── dataman/ # Import/export and backup management
│ ├── db_json_bridge.py # Convert DB ↔ JSON
│ ├── export_db_to_csv.py # Export DB tables to CSV
│ ├── export_tools.py # Interactive export utilities
│ └── safe_restore.py # Safely restore DB from JSON
│
├── tui/ # Text-based interface (menus, prompts)
│ ├── menu_actions.py # Handles user menu selections
│ ├── prompts.py # Input prompts for adding/editing data
│ ├── delete_preview.py # Safe delete with preview
│ └── tui_helpers.py # Common TUI helper functions
│
├── viz/ # Visualization tools
│ └── plot_tree.py # Plots requirement tree relationships
│
├── tests/ # Automated test scripts
│ ├── test_db_json_roundtrip.py
│ └── populate_test_data.py # Fills DB with example data
│
├── data/ # Stores runtime data
│ └── db_name.txt # Name of DB
│
└── README.md
```

## 9) Decision Tree
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/db-decision-tree-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/db-decision-tree-light.png">
  <img alt="Decision Tree" src="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/db-decision-tree-dark.png">
</picture>