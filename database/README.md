# FLA402 Database — Beginner‑Friendly Guide

This README walks you through setting up, using, exporting, and verifying your SQLite requirements database — even if you’ve never touched SQLite or Python before.

> **Tip:** Commands work on Windows, macOS, and Linux. If you see `python`, and your system uses `python3`, swap it accordingly.

---

## 0) What’s in this project?

* **SQLite database** with tables for goals, requirements (swarm/system/subsystem), verification methods, documents, items, joins, etc.
* **TUI (text‑menu) app** to add/search/update/delete rows.
* **JSON export/restore** so you can store changes in Git and review diffs easily.
* **Round‑trip test** (DB → JSON → DB) to ensure integrity.
* **Graph plotter** to visualize requirement links as a tree.

Key scripts:

* `setup_database.py` — create a new `.db` and all tables, write the DB name to `db_name.txt`.
* `run_database.py` — the interactive menu (insert/search/update/delete/export/restore/verify/plot).
* `populate_test_data.py` — optional: fill the DB with demo data.
* `db_json_bridge.py` — export DB → JSON and restore JSON → DB (also has a Command Line Interface (CLI)).
* `verify_roundtrip.py` and `tests/test_db_json_roundtrip.py` — integrity checks.
* `plot_tree.py` — draw the hierarchy (and optionally include methods/documents).

> The file `db_name.txt` is the single source of truth for which DB the tools act on. Change that file to switch DBs.

---

## 1) Prerequisites

1. **Python 3.10+** installed
2. (Optional but recommended) A virtual environment
3. VS Code (recommended) and the **SQLite** extension if you want to browse the DB visually

### Create & activate a virtual environment

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
. .venv\Scripts\activate
```

No external packages are required beyond Python’s standard library and `matplotlib`/`networkx` for plotting. If you plan to use plotting:

```bash
pip install matplotlib networkx
```

---

## 2) First‑time setup (create a brand‑new DB)

This creates a database file and all required tables.

```bash
python setup_database.py
```

Follow the prompts:

* Enter a name like `IRDS_requirements.db` (must end with `.db`).
* If the file exists, you’ll be asked whether to overwrite.
* The script writes the chosen name into `db_name.txt` and creates all tables.

You should now see your `.db` file in the folder.

> Want a different DB later? Edit `db_name.txt` (single line with the path/filename), or run `setup_database.py` again with a new name.

---

## 3) (Optional) Load demo/test data

If you want some sample content to click around with:

```bash
python populate_test_data.py
```

This reads `db_name.txt`, ensures tables exist, and inserts a small demo set of goals/requirements/methods/documents and relationships.

---

## 4) Start the interactive app (TUI)

Run the menu‑driven app:

```bash
python run_database.py
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

## 5) Export DB → JSON (for Git diffs)

Why JSON? It produces clean diffs in pull requests and preserves relationships.

### Option A — from the menu

1. Run `python run_database.py`
2. Choose **Export DB → JSON**
3. Pick an output path (default `database_dump.json`)

### Option B — command‑line (direct)

```bash
# Dump DB → JSON
python db_json_bridge.py dump IRDS_requirements.db database_dump.json
```

The JSON contains:

* `meta` (export timestamp, source DB)
* For each table: column list and all rows
* Any BLOBs are base64‑encoded so they’re JSON‑safe

Commit the JSON to Git to review changes over time.

---

## 6) Restore JSON → DB (to get back the latest data)

### Option A — from the menu

1. Run `python run_database.py`
2. Choose **Restore JSON → DB**
3. Provide the JSON path and the target DB path (press Enter to reuse the current DB)
4. Choose whether to overwrite if it exists

### Option B — command‑line (direct)

```bash
# Restore JSON → DB (add --overwrite if you want to replace an existing file)
python db_json_bridge.py restore database_dump.json IRDS_requirements.db --overwrite
```

During restore:

* The canonical schema is (re)created.
* Self‑referencing tables (system/subsystem requirements) are inserted in safe phases.

---

## 7) Verify the JSON round‑trip

Ensures **DB → JSON → DB** yields identical tables, columns, and rows.

### One‑click (no pytest required)

```bash
python verify_roundtrip.py
```

It reads `db_name.txt`, creates temp files, and compares both databases. You’ll see **PASSED** or a descriptive error.

### With pytest

```bash
pip install pytest
pytest -q
```

This runs `tests/test_db_json_roundtrip.py` which performs the same end‑to‑end check in a test harness.

---

## 8) Plot the requirement tree

To visualize relationships:

```bash
python -c "import plot_tree; plot_tree.run_tree_plot()"
# or simply choose "Plot tree" from run_database.py
```

You’ll be asked whether to include verification methods and documents, then to pick a node type and an ID (or `all`), and a depth cutoff. A window opens with the graph (or images are saved if you choose `all`).

> If you plan to use plotting, make sure you installed `matplotlib` and `networkx` (see prerequisites).

---

## 9) Repo hygiene tips

* Keep `db_name.txt` checked in with a **sensible default** (or add it to `.gitignore` if you prefer per‑user DBs). Everyone’s tools read that file.
* Commit `database_dump.json` updates when you change data so reviewers can see diffs.
* Use branches when making large data edits (e.g., `feature/database‑VVM`).

---

## 10) Troubleshooting

**Foreign key constraint failed**

* You may have inserted a child that references a non‑existent parent. Create the parent first.

**“Author and reviewer must be different” error**

* Choose different people for `author` and `reviewer`.

**“Verification method must be provided if status is not pending”**

* Add the method first (Insert V&V Method), then reference its ID when you set a non‑Pending status.

**Restore complains about unresolved parents**

* Your JSON may contain a parent that’s missing. Fix the source DB/JSON, or insert missing parents first.

**Matplotlib window doesn’t show**

* In VS Code, try running the plot command in an external terminal, or save figures by typing `all` when prompted (files will be written to the project folder).

**Switching databases**

* Edit `db_name.txt` or run `setup_database.py` again to create a new one.

---

## 11) Handy copy‑paste snippets

Create DB & tables

```bash
python setup_database.py
```

Run interactive menu

```bash
python run_database.py
```

Export DB → JSON

```bash
python db_json_bridge.py dump IRDS_requirements.db database_dump.json
```

Restore JSON → DB (overwrite)

```bash
python db_json_bridge.py restore database_dump.json IRDS_requirements.db --overwrite
```

Verify round‑trip

```bash
python verify_roundtrip.py
# or
pytest -q
```

Plot tree

```bash
python -c "import plot_tree; plot_tree.run_tree_plot()"
```

Load demo data

```bash
python populate_test_data.py
```

---

## 12) File/Folder overview

```
.
├── create_tables.py
├── connect_database.py
├── db_json_bridge.py
├── db_utilities.py
├── insert_functions.py
├── plot_tree.py
├── populate_test_data.py
├── prompts.py
├── run_database.py
├── setup_database.py
├── verify_roundtrip.py
├── test_db_json_roundtrip.py
├── db_name.txt        # points to your active .db
└── IRDS_requirements.db (example)
```

You’re set! 🎉 If anything feels unclear, open an issue or ping me and we’ll tighten the docs further.
