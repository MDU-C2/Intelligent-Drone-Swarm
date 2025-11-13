# export_tools.py
from pathlib import Path
import sqlite3
import mimetypes
from ..dataman.db_json_bridge import dump_db_to_json
from ..dataman.export_db_to_csv import export_db_to_csv
from database.core.paths import DATA_DIR, JSON_DUMP, CSV_DIR, DB_NAME_TXT

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
    And also export all document BLOBs into:
        database/data/csv_exports/documents/
    """
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    export_db_to_csv(str(CSV_DIR))  # delimiter=';' already set in your exporter

    # NEW: export all document files alongside the CSVs
    try:
        _export_all_documents_to_csv_folder()
    except Exception as e:
        # Don't break CSV export if docs fail – just warn
        print(f"⚠️ Document export failed: {e}")

    print(f"✅ Exported CSVs → {CSV_DIR}")


def _ext_from_mime(mime: str | None) -> str:
    if not mime:
        return ".bin"
    # guess_extension may return None or odd variants; guard it
    ext = mimetypes.guess_extension(mime) or ""
    return ext if ext else ".bin"

def _export_all_documents_to_csv_folder() -> None:
    """
    Export every document BLOB in the 'documents' table into
    database/data/csv_exports/documents/
    (or whatever CSV_DIR is configured to).

    Each file is named by export_document_file(), using the stored
    file_name/mime_type/title.
    """
    # Ensure we have an active DB
    if not DB_NAME_TXT.exists():
        print(f"⚠️ {DB_NAME_TXT} not found — skipping document export.")
        return

    db_path = DB_NAME_TXT.read_text().strip()
    if not db_path:
        print("⚠️ db_name.txt is empty — skipping document export.")
        return

    docs_dir = CSV_DIR / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Collect all document IDs
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("SELECT doc_id FROM documents ORDER BY doc_id;")
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(f"⚠️ Could not query documents table: {e}")
        conn.close()
        return

    conn.close()

    if not rows:
        print("ℹ️ No documents found — nothing to export.")
        return

    print(f"\n→ Exporting {len(rows)} document file(s) to {docs_dir} …")

    for (doc_id,) in rows:
        # Ensure doc_id is passed as string (export_document_file expects str)
        export_document_file(str(db_path), str(doc_id), output_dir=str(docs_dir))

    print(f"✅ Exported {len(rows)} document file(s) → {docs_dir}")

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
