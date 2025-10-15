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

## 2) First‑time setup (create a brand‑new DB)

This creates a database file and all required tables.
Open a Terminal in VS Code:

```bash
python -m database.app.setup_database.py
```

Follow the prompts:

* Enter a name like `IRDS_requirements.db` (must end with `.db`).
* If the file exists, you’ll be asked whether to overwrite.
* The script writes the chosen name into `db_name.txt` and creates all tables.

You should now see your `.db` file in the folder.

---

## 3) Start the interactive app

Run the menu‑driven app:

```bash
python -m database.app.run_database
```

You’ll see numbered actions like **Insert Goal**, **Insert System Requirement**, **Search**, **Export DB → JSON**, **Restore JSON → DB**, **Verify round‑trip**, **Plot tree**, etc. Type the number and follow the prompts. Type `exit` during a prompt to cancel and return to the main menu.

### Notes while inserting data

* **Authors vs. Reviewers:** they must be different (the tool enforces this).
* **Verification status:** if not `Pending`, you must supply a verification method ID that already exists.
* Many fields use fixed choices (e.g., `Priority` is `Key/Mandatory/Optional`; statuses have limited options). Follow the on‑screen hints.

### Search, Update, Delete

* **Search** lets you interactively pick a table/column and look for exact or partial matches.
* **Update/Delete** walk you through choosing the table, the row by its ID, then the column/value.

---

## 4) Export DB → JSON (for GitHub diffs)

Why JSON? It produces clean diffs in pull requests and **preserves relationships**.

1. Run `python -m database.app.run_database`
2. Choose **Export DB → JSON**

The JSON contains:

* `meta` (export timestamp, source DB)
* For each table: column list and all rows
* Any BLOBs are base64‑encoded so they’re JSON‑safe

Commit the JSON to GitHub to review changes over time.

---

## 5) How to restore JSON → DB (to get the latest data)

1. Run `python -m database.app.run_database`
2. Choose **Restore JSON → DB**
3. Follow the instructions
4. The command you will be told to use is `python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/IRDS_requirements.db --overwrite`

During restore:

* The canonical schema is (re)created.
* Self‑referencing tables (system/subsystem requirements) are inserted in safe phases.

---

## 6) Repo hygiene tips

* Commit `database_dump.json` updates when you change data so reviewers can see diffs.
* Use branches when making large data edits (e.g., `feature/database‑VVM`).

---

## 7) Troubleshooting

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

## 8) Handy copy‑paste snippets

Create DB & tables

```bash
python -m database.app.setup_database
```

Run interactive menu

```bash
python -m database.app.run_database
```

Load demo data

```bash
python -m database.app.populate_test_data
```

---

## 9) File/Folder overview

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
│ └── db_utilities.py # Shared database utility functions
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
