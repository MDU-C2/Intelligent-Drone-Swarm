# Beginner‑Friendly Guide to the Database

This README walks you through setting up, using, exporting, and verifying our SQLite requirements database — even if you’ve never touched SQLite or Python before.

### NOTE
- Our **main** database is **IRDS_requirements.db** located in the branch `feature/database`
- A graphical representation of the work flow can be seen at the bottom of this page *(Decisions Tree)*

---

## What’s in the database folder?

* **SQLite database** with tables for goals, requirements (swarm/system/subsystem), verification methods, documents, items, joins, etc.
* **JSON export/restore** so we can store changes in Git and review differences easily.
* **Graph plotter** to visualize requirement links as a tree.

Key scripts:

* `setup_database.py` — create a local `.db` and write filepath to and name of the local DB to `db_name.txt`.
* `db_json_bridge` — pull contents of main database to local database
* `run_database.py` — the interactive menu (insert/search/update/delete/export/restore/verify/plot).

---

## Prerequisites

1. **Python 3.10+** installed *(not 3.13 though)*
    * *Alternatively, create an environment for the database using Anaconda*
2. **VS Code** with the **SQLite** extension

---

## 1) Start using the database

1. Create your own branch from the branch `feature/database` (example: `feature/database-VVM`)
2. Open your branch in VS Code
3. Open a Terminal in VS Code and run:
(press ENTER instead of inserting a .db name)
```bash
python -m database.app.setup_database
```
4. In the same Terminal run:
```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/local.db --overwrite
```


6. Right-click on `local.db` (in the `data` folder) and choose "Open Database" to see the content of the database
7. In the Terminal run:
```bash
python -m database.app.run_database
```
6. Follow the prompts
(Type `exit` during a prompt to cancel and return to the main menu.)
7. When you're done **inserting data** follow the instructions under **2) Export DB → JSON, and then push to GitHub**

### Notes while inserting data

* **Authors vs. Reviewers:** they must be different *(this is enforced in the code)*.
* **Verification status:** if not `Pending`, you must supply a verification method ID that already exists.

---

## 2) Export DB → JSON, and then push to GitHub
(still on your own branch in VS Code)
1. In the Terminal run `python -m database.app.run_database`
1. Choose **Export DB → JSON**
1. Exit
1. Make sure `database_dump.json` is marked as modified *(M, orange)*
1. Delete `local.db` *(or just don't push this file to GitHub)*
1. **Commit** your changes *to your local branch*
1. **Push** your changes to GitHub and open a **Pull Request** requesting to merge your branch to `feature/database` *(files changed should be: database_dump.json, and possibly db_name.txt)*
1. If there are no conflicts you can go ahead and squash merge. But if there are conflicts ask for help from the Chief Engineer ;)

**Note:** The Chief Engineer and/or the Requirements Manager are in charge of inserting `database_dump.json` to `IRDS_requirements.db` in the `feature/database` branch :)

---

## Troubleshooting

**Foreign key constraint failed**

* You may have inserted a child that references a non‑existent parent. Create the parent first.

**“Author and verifier must be different” error**

* Choose different people for `author` and `verifier`.

**“Verification method must be provided if status is not pending”**

* Add the method first (Insert V&V Method), then reference its ID when you set a non‑Pending status.

**Restore complains about unresolved parents**

* Your JSON may contain a parent that’s missing. Fix the source DB/JSON, or insert missing parents first.

**Matplotlib window doesn’t show**

* In VS Code save figures by typing `all` when prompted (files will be written to the data folder).

---

## Handy copy‑paste snippets

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
## Restoring JSON → DB
**For CE/RM eyes only**
1. Open `feature/database` in VS Code
    * *Note: Might have to fix filepath in db_name.txt*
2. Open a Terminal and run:
```bash
python -m database.dataman.db_json_bridge restore database/data/database_dump.json database/data/IRDS_requirements.db --overwrite
```
3. Push changes to GitHub (`IRDS_requirements.db`, and possibly `db_name.txt`, should be the only change)
4. Done!

---
## Other

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

## File/Folder overview

### database/app
Entry point scripts.
- `app/run_database.py`
  Main interactive interface
- `app/setup_database.py`
  Sanitizes filepath, creates database and tables
- `app/verify_roundtrip.py`
  Tests DB ↔ JSON conversion integrity

### database/core
Core database logic and schema
- `core/connect_database.py`
  Handles database connections
- `core/create_tables.py`
  Defines tables and foreign keys
- `core/db_utilities.py`
  delete_from_table, update_row, interactive_search
- `core/insert_functions.py`
  Insert helpers for each table
- `core/paths.py`
  Paths used

### database/data

- `data/IRDS_requirements.db`
  Main database
- `data/database_dump.json`
  JSON version of main database
- `data/db_name.txt`
  Filepath to and name of DB
- `data/local.db`
  Local database

### database/dataman
Import/export and backup management
- `dataman/db_json_bridge.py`
  Convert DB ↔ JSON
- `dataman/export_db_to_csv.py`
  Export DB tables to CSV (Excel)
- `dataman/export_tools.py`
  export_db_to_json_interactive, export_db_to_csv_interactive
- `dataman/safe_restore.py`
  Safe restore helper for Windows (avoids file-lock issues during DB restore)

### database/tests
Automated test scripts
- `tests/pop_test_data.py`
  Fills DB with example data
- `tests/populate_test_data.py`
  Fills DB with example data
- `tests/test_db_json_roundtrip.py`

### database/tui
Text-based interface (menus, prompts)
- `tui/delete_preview.py`
  Safe delete with preview
- `tui/menu_actions.py`
  Handlers for TUI actions to keep run_database.py uncluttered
- `tui/prompts.py`
  Input prompts for adding/editing data
- `tui/tui_helpers.py`
  wait_for_enter

### database/viz

- `viz/plot_tree.py`
  Plots requirement tree relationships

---

## Decision Tree
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/db-decision-tree-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/db-decision-tree-light.png">
  <img alt="Decision Tree" src="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/db-decision-tree-dark.png">
</picture>