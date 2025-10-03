# insert_prompts.py

def prompt_input(prompt_text, optional=False):
    """Helper to allow typing 'exit' to return to menu"""
    value = input(prompt_text)
    if value.lower() == "exit":
        return "EXIT"
    if optional and value == "":
        return None
    return value

# ----- Prompts for main tables -----
def prompt_goal():
    print("\nEnter new goal (type 'exit' to return to menu):")
    data = {
        "goal_id": prompt_input("Goal ID: "),
        "goal_description": prompt_input("Description: "),
        "stakeholder": prompt_input("Stakeholder: "),
        "origin": prompt_input("Origin: "),
        "priority": prompt_input("Priority (Key/Mandatory/Optional): "),
        "rationale": prompt_input("Rationale: "),
        "satisfaction_status": prompt_input("Satisfaction status (Pending/Not satisfied/Satisfied): "),
        "method_id": prompt_input("Method ID (optional): ", optional=True)
    }
    if "EXIT" in data.values(): return None
    return data

def prompt_drone_swarm_requirement():
    print("\nEnter new drone swarm requirement (type 'exit' to return to menu):")
    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H): ")
    if author == "EXIT": return None
    reviewer = prompt_input("Reviewer (different from author): ")
    if reviewer == "EXIT": return None
    verification_status = prompt_input("Verification status (Pending/Failed/Verified/Inconclusive): ")
    if verification_status == "EXIT": return None
    verification_method = prompt_input("Verification method ID (optional): ", optional=True)
    if verification_method == "EXIT": return None

    data = {
        "swarm_req_id": prompt_input("Swarm Req ID: "),
        "requirement": prompt_input("Requirement description: "),
        "priority": prompt_input("Priority (Key/Mandatory/Optional): "),
        "effect": prompt_input("Effect: "),
        "rationale": prompt_input("Rationale: "),
        "author": author,
        "review_status": prompt_input("Review status (TBR/Reviewed/Accepted/Rejected): "),
        "reviewer": reviewer,
        "verification_status": verification_status,
        "verification_method": verification_method,
        "comment": prompt_input("Comment (optional): ", optional=True)
    }
    if "EXIT" in data.values(): return None
    return data

def prompt_goal_children():
    print("\nLink goal and swarm requirement (goal_children table):")
    goal_id = prompt_input("Goal ID: ")
    if goal_id == "EXIT": return None
    swarm_req_id = prompt_input("Swarm Req ID: ")
    if swarm_req_id == "EXIT": return None
    return {"goal_id": goal_id, "swarm_req_id": swarm_req_id}

def prompt_swarm_req_children():
    print("\nLink swarm requirement and system requirement (swarm_req_children table):")
    swarm_req_id = prompt_input("Swarm Req ID: ")
    if swarm_req_id == "EXIT": return None
    sys_req_id = prompt_input("System Req ID: ")
    if sys_req_id == "EXIT": return None
    return {"swarm_req_id": swarm_req_id, "sys_req_id": sys_req_id}

def prompt_sysreq_children():
    print("\nLink system requirement and subsystem requirement (sysreq_children table):")
    sys_req_id = prompt_input("System Req ID: ")
    if sys_req_id == "EXIT": return None
    sub_req_id = prompt_input("Subsystem Req ID: ")
    if sub_req_id == "EXIT": return None
    return {"sys_req_id": sys_req_id, "sub_req_id": sub_req_id}

def prompt_subsys_join_item():
    print("\nLink subsystem requirement and item (sys_join_item table):")
    item_id = prompt_input("Item ID: ")
    if item_id == "EXIT": return None
    sub_req_id = prompt_input("Subsystem Req ID: ")
    if sub_req_id == "EXIT": return None
    return {"item_id": item_id, "sub_req_id": sub_req_id}

def prompt_V_join_documents():
    print("\nLink test/verification and document (V_join_documents table):")
    method_id = prompt_input("Method ID: ")
    if method_id == "EXIT": return None
    doc_id = prompt_input("Document ID: ")
    if doc_id == "EXIT": return None
    return {"method_id": method_id, "doc_id": doc_id}

def prompt_quality_requirements():
    print("\nInsert quality requirement:")
    quality_rec_id = prompt_input("Quality Requirement ID: ")
    if quality_rec_id == "EXIT": return None
    requirement = prompt_input("Requirement description: ")
    if requirement == "EXIT": return None
    author = prompt_input("Author (E.Z/C.N/Y.M.B/E.M/A.H): ")
    if author == "EXIT": return None
    approved_by = prompt_input("Approved by (Y.M.B or empty): ", optional=True)
    if approved_by == "EXIT": return None
    return {"quality_rec_id": quality_rec_id, "requirement": requirement, "author": author, "approved_by": approved_by}

def prompt_id_glossary():
    print("\nInsert glossary entry:")
    prefix = prompt_input("Prefix: ")
    if prefix == "EXIT": return None
    meaning = prompt_input("Meaning: ")
    if meaning == "EXIT": return None
    return {"prefix": prefix, "meaning": meaning}
