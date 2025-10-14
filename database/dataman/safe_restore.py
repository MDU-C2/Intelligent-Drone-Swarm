# safe_restore.py
"""
Safe restore helper for Windows (avoids file-lock issues during DB restore).

Used by run_database.py when user chooses "Restore JSON → DB".
"""

import os
import uuid
from ..dataman.db_json_bridge import restore_db_from_json


def safe_restore_from_json(current_db: str, in_path: str, target_db: str, overwrite: bool) -> str:
    """
    Safely restores JSON → DB, handling locked files on Windows.

    Returns:
        - "exit" if the TUI should exit (because the DB was replaced)
        - "continue" if it's safe to keep running
    """
    try:
        if overwrite and target_db == current_db:
            # Can't overwrite the DB while it’s open
            base, ext = os.path.splitext(current_db)
            new_db = f"{base}.restored-{uuid.uuid4().hex[:8]}{ext}"

            print(f"\n[Info] '{current_db}' is currently open. Restoring to a new file instead:")
            print(f"       → {new_db}")
            restore_db_from_json(new_db, in_path, overwrite=True)

            with open("db_name.txt", "w", encoding="utf-8") as f:
                f.write(new_db)

            print(f"\n✅ Restored to '{new_db}' and updated db_name.txt.")
            print("ℹ️  The app will now exit to release the old file. Re-run run_database.py to use the restored DB.")
            return "exit"

        else:
            # Safe case: restoring to a different file
            restore_db_from_json(target_db, in_path, overwrite=overwrite)
            print(f"Restored '{target_db}' from '{in_path}' (overwrite={overwrite})")

            if target_db != current_db:
                use_now = input(f"\nSwitch to '{target_db}' now? (y/N): ").strip().lower() == "y"
                if use_now:
                    with open("db_name.txt", "w", encoding="utf-8") as f:
                        f.write(target_db)
                    print("✅ Updated db_name.txt. The app will exit; restart to use the new DB.")
                    return "exit"

            return "continue"

    except Exception as e:
        print(f"Restore failed: {e}")
        return "continue"
