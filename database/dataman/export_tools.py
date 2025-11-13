# export_tools.py
from pathlib import Path
import sqlite3
import mimetypes
from ..dataman.db_json_bridge import dump_db_to_json
from ..dataman.export_db_to_csv import export_db_to_csv
from database.core.paths import DATA_DIR, JSON_DUMP, CSV_DIR

def export_db_to_json_interactive(db_name: str) -> None:
    """
    Export DB → JSON to a fixed, non-overridable path:
        database/data/database_dump.json
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dump_db_to_json(db_name, str(JSON_DUMP))
    print(f"✅ Exported JSON → {JSON_DUMP}")

def export_db_to_csv_interactive() -> None:
    """
    Export all tables → CSVs into a fixed folder:
        database/data/csv_exports/
    """
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    export_db_to_csv(str(CSV_DIR))  # delimiter=';' already set in your exporter
    print(f"✅ Exported CSVs → {CSV_DIR}")

def _ext_from_mime(mime: str | None) -> str:
    if not mime:
        return ".bin"
    # guess_extension may return None or odd variants; guard it
    ext = mimetypes.guess_extension(mime) or ""
    return ext if ext else ".bin"

def export_document_file(db_path: str, doc_id: str, output_dir: str = ".") -> Path | None:
    """
    Export the BLOB from documents.file for the given doc_id.
    Uses stored file_name and mime_type to name the file.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT title, file, file_name, mime_type
        FROM documents
        WHERE doc_id = ?
    """, (doc_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        print(f"❌ No document found with ID '{doc_id}'.")
        return None

    title, file_bytes, file_name, mime_type = row
    if file_bytes is None:
        print(f"⚠️ Document '{doc_id}' has no file stored.")
        return None

    # Prefer stored filename; otherwise synthesize one from doc_id + MIME
    if file_name:
        out_name = file_name
    else:
        # sanitize title for nicer fallback names (optional)
        safe_title = "".join(c for c in (title or "") if c.isalnum() or c in (" ", "_", "-")).strip()
        ext = _ext_from_mime(mime_type)
        base = f"{doc_id}_{safe_title}" if safe_title else f"{doc_id}"
        out_name = base + ext

    out_path = out_dir / out_name
    with out_path.open("wb") as f:
        f.write(file_bytes)

    print(f"✅ Exported to: {out_path}")
    return out_path
