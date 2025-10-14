# delete_preview.py
"""
Preview & confirm deletes with cascade awareness.

Assumes your updated schema:
- Join tables CASCADE on delete
- parent_id in system/subsystem uses ON DELETE SET NULL
- verification_method/method_id uses ON DELETE SET NULL
"""

from connect_database import connect_database
from typing import Dict, Tuple, List


def _fetch_one(cur, sql: str, params=()) -> int:
    cur.execute(sql, params)
    row = cur.fetchone()
    return int(row[0]) if row and row[0] is not None else 0


def _fetch_list(cur, sql: str, params=()) -> List[Tuple]:
    cur.execute(sql, params)
    return list(cur.fetchall())


def preview_goal(cur, goal_id: str) -> Dict:
    # CASCADE: goal_children rows by goal_id will be removed
    links = _fetch_list(cur, "SELECT id, swarm_req_id FROM goal_children WHERE goal_id = ?", (goal_id,))
    return {
        "entity": ("goals", "goal_id", goal_id),
        "cascade_links": {
            "goal_children": {"count": len(links), "sample": links[:10]}
        },
        "detach": {},  # none for goals
        "set_null": {} # none for goals
    }


def preview_swarm(cur, swarm_req_id: str) -> Dict:
    gc = _fetch_list(cur, "SELECT id, goal_id FROM goal_children WHERE swarm_req_id = ?", (swarm_req_id,))
    src = _fetch_list(cur, "SELECT id, sys_req_id FROM swarm_req_children WHERE swarm_req_id = ?", (swarm_req_id,))
    return {
        "entity": ("drone_swarm_requirements", "swarm_req_id", swarm_req_id),
        "cascade_links": {
            "goal_children": {"count": len(gc), "sample": gc[:10]},
            "swarm_req_children": {"count": len(src), "sample": src[:10]},
        },
        "detach": {},  # none specific
        "set_null": {} # verification_method is SET NULL but we don't need a count here
    }


def preview_system(cur, sys_req_id: str) -> Dict:
    # CASCADE links
    src = _fetch_list(cur, "SELECT id, swarm_req_id FROM swarm_req_children WHERE sys_req_id = ?", (sys_req_id,))
    syc = _fetch_list(cur, "SELECT id, sub_req_id FROM sysreq_children WHERE sys_req_id = ?", (sys_req_id,))
    # SET NULL dependents (children that list this as parent_id)
    det = _fetch_list(cur, "SELECT sys_req_id FROM system_requirements WHERE parent_id = ?", (sys_req_id,))
    return {
        "entity": ("system_requirements", "sys_req_id", sys_req_id),
        "cascade_links": {
            "swarm_req_children": {"count": len(src), "sample": src[:10]},
            "sysreq_children": {"count": len(syc), "sample": syc[:10]},
        },
        "detach": {
            "system_requirements.children(parent_id)": {"count": len(det), "sample": det[:10]},
        },
        "set_null": {}
    }


def preview_subsystem(cur, sub_req_id: str) -> Dict:
    # CASCADE links
    syc = _fetch_list(cur, "SELECT id, sys_req_id FROM sysreq_children WHERE sub_req_id = ?", (sub_req_id,))
    sji = _fetch_list(cur, "SELECT id, item_id FROM sys_join_item WHERE sub_req_id = ?", (sub_req_id,))
    # SET NULL dependents
    det = _fetch_list(cur, "SELECT sub_req_id FROM subsystem_requirements WHERE parent_id = ?", (sub_req_id,))
    return {
        "entity": ("subsystem_requirements", "sub_req_id", sub_req_id),
        "cascade_links": {
            "sysreq_children": {"count": len(syc), "sample": syc[:10]},
            "sys_join_item": {"count": len(sji), "sample": sji[:10]},
        },
        "detach": {
            "subsystem_requirements.children(parent_id)": {"count": len(det), "sample": det[:10]},
        },
        "set_null": {}
    }


def preview_method(cur, method_id: str) -> Dict:
    # CASCADE links
    vjd = _fetch_list(cur, "SELECT id, doc_id FROM V_join_documents WHERE method_id = ?", (method_id,))
    # SET NULL refs (we won’t list all, but show counts)
    g = _fetch_one(cur, "SELECT COUNT(*) FROM goals WHERE method_id = ?", (method_id,))
    sw = _fetch_one(cur, "SELECT COUNT(*) FROM drone_swarm_requirements WHERE verification_method = ?", (method_id,))
    sy = _fetch_one(cur, "SELECT COUNT(*) FROM system_requirements WHERE verification_method = ?", (method_id,))
    ss = _fetch_one(cur, "SELECT COUNT(*) FROM subsystem_requirements WHERE verification_method = ?", (method_id,))
    return {
        "entity": ("test_and_verification", "method_id", method_id),
        "cascade_links": {
            "V_join_documents": {"count": len(vjd), "sample": vjd[:10]},
        },
        "detach": {},
        "set_null": {
            "goals.method_id": g,
            "drone_swarm_requirements.verification_method": sw,
            "system_requirements.verification_method": sy,
            "subsystem_requirements.verification_method": ss,
        }
    }


def preview_delete(entity_type: str, entity_id: str) -> Dict:
    """
    entity_type: one of 'goal','swarm','system','subsystem','method'
    """
    with open("db_name.txt") as f:
        db_name = f.read().strip()
    with connect_database(db_name) as db:
        if entity_type == "goal":
            return preview_goal(db.cursor, entity_id)
        if entity_type == "swarm":
            return preview_swarm(db.cursor, entity_id)
        if entity_type == "system":
            return preview_system(db.cursor, entity_id)
        if entity_type == "subsystem":
            return preview_subsystem(db.cursor, entity_id)
        if entity_type == "method":
            return preview_method(db.cursor, entity_id)
        raise ValueError(f"Unsupported entity_type: {entity_type}")


def perform_delete(preview: Dict) -> int:
    """
    Executes the delete for the previewed entity.
    Returns number of core rows deleted (0 or 1). Cascades happen automatically.
    """
    table, id_col, entity_id = preview["entity"]
    with open("db_name.txt") as f:
        db_name = f.read().strip()
    with connect_database(db_name) as db:
        db.cursor.execute(f"DELETE FROM {table} WHERE {id_col} = ?", (entity_id,))
        return db.cursor.rowcount


def print_preview(p: Dict) -> None:
    table, id_col, entity_id = p["entity"]
    print(f"\nDelete preview for {table}.{id_col} = {entity_id}\n" + "-"*55)

    if p["cascade_links"]:
        print("• Link rows that will be REMOVED (via CASCADE):")
        for t, info in p["cascade_links"].items():
            print(f"  - {t}: {info['count']} row(s)")
            for sample in info["sample"]:
                print(f"      sample: {sample}")
    else:
        print("• No link rows will be removed.")

    if p["detach"]:
        print("\n• Children that will be DETACHED (parent_id → NULL):")
        for label, info in p["detach"].items():
            print(f"  - {label}: {info['count']} row(s)")
            for sample in info["sample"]:
                print(f"      sample: {sample}")
    else:
        print("\n• No children will be detached.")

    if p["set_null"]:
        print("\n• References that will be SET TO NULL:")
        for label, count in p["set_null"].items():
            print(f"  - {label}: {count} row(s)")
    else:
        print("\n• No references will be set to NULL.")
