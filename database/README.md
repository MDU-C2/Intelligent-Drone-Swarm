# Beginner‑Friendly Guide to the Database

This README walks you through setting up, using, exporting, and verifying our SQLite requirements database — even if you’ve never touched SQLite or Python before.

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

1. Create your own branch from the branch `feature/database` (example: feature/database-VVM)
2. Open your branch in VS Code
3. Open a Terminal and run:
```bash
python -m database.app.setup_database
```
(This will create your own local copy of the database (do not pick `IRDS_requirements` as the name of your db)

4. In the Terminal run:

```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/{NAME-OF-YOUR-DB}.db --overwrite
```
Switch out `{NAME-OF-YOUR-DB}`with the name you chose for your db

4. Right-click on `{NAME-OF-YOUR-DB}.db` (in the `data` folder) and choose "Open Database"
5. In the Terminal run:
```bash
python -m database.app.run_database
```
6. Follow the prompts
(Type `exit` during a prompt to cancel and return to the main menu.)
7. When you're done inputting data follow the instructions under **3) Export DB → JSON, and then push to GitHub**

### Notes while inserting data

* **Authors vs. Reviewers:** they must be different *(this is enforced in the code)*.
* **Verification status:** if not `Pending`, you must supply a verification method ID that already exists.
* Many fields use fixed choices (e.g., `Priority` is `Key/Mandatory/Optional`; statuses have limited options). Follow the on‑screen hints.

### Search, Update, Delete

* **Search** lets you interactively pick a table/column and look for exact or partial matches.
* **Update/Delete** walks you through choosing the table, the row by its ID, then the column/value.

---

## 3) Export DB → JSON, and then push to GitHub
(still on your own branch in VS Code)
1. In the Terminal run `python -m database.app.run_database`
2. Choose **Export DB → JSON**
3. Exit `run_database`
4. Delete `{NAME-OF-YOUR-DB}.db` and keep `database_dump.json`
5. Commit your changes
6. Push your changes to GitHub and open a Pull Request requesting to merge your branch to `feature/database`
7. If there are no conflicts you can go ahead and squash merge. But if there are conflicts ask for help from the Chief Engineer ;)

**Note:** The Chief Engineer and/or the Requirements Manager are in charge of restoring the `database_dump.json` to `IRDS_requirements.db` in the `feature/database` branch :)

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

Set up local database (do not pick `IRDS_requirements` as the name of your db)
```bash
python -m database.app.setup_database
```

Load JSON to DB (switch out `{NAME-OF-YOUR-DB}`with the name you chose for your db)
```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/{NAME-OF-YOUR-DB}.db --overwrite
```

Run interactive menu
```bash
python -m database.app.run_database
```

Create DB & tables
```bash
python -m database.app.setup_database
```

Load demo data
```bash
python -m database.tests.populate_test_data
```

---

## 6) File/Folder overview

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

---
## 7) First‑time setup (create a brand‑new DB)
**Note:** Only the CE or the RM does this.

This creates a database file and all required tables.
Open a Terminal in VS Code:

```bash
python -m database.app.setup_database.py
```

Follow the prompts:

* Enter a name like `IRDS_requirements`.
* If the file exists, you’ll be asked whether to overwrite.
* The script writes the chosen name into `db_name.txt` and creates all tables.

You should now see your `.db` file in the `data` folder.

---