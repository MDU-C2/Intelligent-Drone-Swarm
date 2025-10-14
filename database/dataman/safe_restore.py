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
            # Step 1: close current DB connection by exiting TUI
            print(f"\n[Info] '{current_db}' is currently open and will be replaced in place.")
            print("→ The app will now close the connection, restore the data, and reopen next run.")

            # Step 2: actually restore (overwrite)
            restore_db_from_json(current_db, in_path, overwrite=True)

            print(f"\n✅ Restored directly into '{current_db}'.")
            print("ℹ️  The app will now exit to ensure the file handle is released.")
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
