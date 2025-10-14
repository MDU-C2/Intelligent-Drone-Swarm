# fix_orphan_parents.py
"""
Find and detach orphaned parent links in:
  - system_requirements (parent_id -> sys_req_id)
  - subsystem_requirements (parent_id -> sub_req_id)

By default it FIXES (sets parent_id=NULL). Use --dry-run to only report.

Usage:
    python fix_orphan_parents.py          # fix in place
    python fix_orphan_parents.py --dry-run
"""

from connect_database import connect_database
import argparse
from pathlib import Path
from typing import List, Tuple


def _find_orphans(cur, table: str, id_col: str, parent_col: str) -> List[Tuple[str, str]]:
    """
    Return list of (child_id, missing_parent_id) for rows whose parent_id
    points to a non-existent parent in the same table.
    """
    sql = f"""
        SELECT child.{id_col}, child.{parent_col}
        FROM {table} AS child
        LEFT JOIN {table} AS parent
          ON child.{parent_col} = parent.{id_col}
        WHERE child.{parent_col} IS NOT NULL
          AND parent.{id_col} IS NULL
        ORDER BY child.{parent_col}, child.{id_col};
    """
    cur.execute(sql)
    return [(row[0], row[1]) for row in cur.fetchall()]


def _detach(cur, table: str, parent_col: str, missing_parents: List[str]) -> int:
    """
    Set parent_id=NULL for all rows whose parent_id is in missing_parents.
    Returns number of rows affected.
    """
    total = 0
    for p in missing_parents:
        cur.execute(f"UPDATE {table} SET {parent_col}=NULL WHERE {parent_col} = ?", (p,))
        total += cur.rowcount
    return total


def main(dry_run: bool) -> None:
    db_path = Path("db_name.txt").read_text().strip()

    tasks = [
        ("system_requirements",  "sys_req_id", "parent_id"),
        ("subsystem_requirements", "sub_req_id", "parent_id"),
    ]

    with connect_database(db_path) as db:
        any_orphans = False

        for table, id_col, parent_col in tasks:
            orphans = _find_orphans(db.cursor, table, id_col, parent_col)
            if not orphans:
                print(f"✅ {table}: no orphaned parents found.")
                continue

            any_orphans = True
            print(f"\n⚠️  {table}: found {len(orphans)} orphaned rows:")
            by_parent = {}
            for child_id, missing_parent in orphans:
                by_parent.setdefault(missing_parent, []).append(child_id)

            for missing_parent, children in by_parent.items():
                print(f"  - Missing parent '{missing_parent}' <- children {children}")

            if not dry_run:
                affected = _detach(db.cursor, table, parent_col, list(by_parent.keys()))
                print(f"   → Fixed {affected} row(s) by setting {parent_col}=NULL.")

        if not any_orphans:
            print("\n🎉 All good — no fixes needed.")
        elif dry_run:
            print("\n🔎 Dry run only — no changes were made.")
        else:
            print("\n✅ Done — orphaned parents detached.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Only report; make no changes.")
    args = ap.parse_args()
    main(dry_run=args.dry_run)
