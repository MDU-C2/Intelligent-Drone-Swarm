# plot_tree.py

import networkx as nx
import matplotlib.pyplot as plt

from pathlib import Path
from ..core.connect_database import connect_database
from ..core.create_tables import create_tables

DB_NAME_PATH = Path(__file__).resolve().parents[1] / "data" / "db_name.txt"

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """Hierarchical layout for a tree (or DAG)."""
    if root is None:
        root = list(G.nodes)[0]

    def _hierarchy_pos(G, root, leftmost, width, vert_gap, vert_loc, xcenter,
                       pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.successors(root))
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, leftmost, dx, vert_gap,
                                     vert_loc-vert_gap, nextx, pos, root)
        return pos

    return _hierarchy_pos(G, root, 0, width, vert_gap, vert_loc, xcenter)

def build_graph(include_methods=True, include_docs=True):
    """Builds the full directed graph from database relationships with type info."""
    G = nx.DiGraph()
    
    with open(DB_NAME_PATH) as f:
        db_name = f.read().strip()

    with connect_database(db_name) as db:
        tables = create_tables(db.cursor)
        tables.create_all_tables()

        
        # goal -> swarm_req
        db.cursor.execute("""
            SELECT goal_id, swarm_req_id FROM goal_children
            WHERE goal_id IS NOT NULL AND swarm_req_id IS NOT NULL
        """)
        for parent, child in db.cursor.fetchall():
            G.add_node(parent, type="goal_id")
            G.add_node(child, type="swarm_req_id")
            G.add_edge(parent, child)

        # swarm_req -> sys_req
        db.cursor.execute("""
            SELECT swarm_req_id, sys_req_id FROM swarm_req_children
            WHERE swarm_req_id IS NOT NULL AND sys_req_id IS NOT NULL
        """)
        for parent, child in db.cursor.fetchall():
            G.add_node(parent, type="swarm_req_id")
            G.add_node(child, type="sys_req_id")
            G.add_edge(parent, child)

        # sys_req (parent -> child sys_req)
        db.cursor.execute("""
            SELECT parent_id, sys_req_id FROM system_requirements
            WHERE parent_id IS NOT NULL AND sys_req_id IS NOT NULL
        """)
        for parent, child in db.cursor.fetchall():
            G.add_node(parent, type="sys_req_id")
            G.add_node(child, type="sys_req_id")
            G.add_edge(parent, child)

        # sys_req -> sub_req
        db.cursor.execute("""
            SELECT sys_req_id, sub_req_id FROM sysreq_children
            WHERE sys_req_id IS NOT NULL AND sub_req_id IS NOT NULL
        """)
        for parent, child in db.cursor.fetchall():
            G.add_node(parent, type="sys_req_id")
            G.add_node(child, type="sub_req_id")
            G.add_edge(parent, child)

        # subsys_req (parent -> child subsys_req)
        db.cursor.execute("""
            SELECT parent_id, sub_req_id FROM subsystem_requirements
            WHERE parent_id IS NOT NULL AND sub_req_id IS NOT NULL
        """)
        for parent, child in db.cursor.fetchall():
            G.add_node(parent, type="sub_req_id")
            G.add_node(child, type="sub_req_id")
            G.add_edge(parent, child)

        if include_methods:
            # goal_id -> method_id
            db.cursor.execute("""
                SELECT goal_id, method_id FROM goals
                WHERE goal_id IS NOT NULL AND method_id IS NOT NULL
            """)
            for parent, child in db.cursor.fetchall():
                G.add_node(parent, type="goal_id")
                G.add_node(child, type="verification_method")
                G.add_edge(parent, child)

            # swarm_req_id -> method_id
            db.cursor.execute("""
                SELECT swarm_req_id, verification_method FROM drone_swarm_requirements
                WHERE swarm_req_id IS NOT NULL AND verification_method IS NOT NULL
            """)
            for parent, child in db.cursor.fetchall():
                G.add_node(parent, type="swarm_req_id")
                G.add_node(child, type="verification_method")
                G.add_edge(parent, child)

            # sys_req_id -> method_id
            db.cursor.execute("""
                SELECT sys_req_id, verification_method FROM system_requirements
                WHERE sys_req_id IS NOT NULL AND verification_method IS NOT NULL
            """)
            for parent, child in db.cursor.fetchall():
                G.add_node(parent, type="sys_req_id")
                G.add_node(child, type="verification_method")
                G.add_edge(parent, child)

            # sub_req_id -> verification_method
            db.cursor.execute("""
                SELECT sub_req_id, verification_method FROM subsystem_requirements
                WHERE sub_req_id IS NOT NULL AND verification_method IS NOT NULL
            """)
            for parent, child in db.cursor.fetchall():
                G.add_node(parent, type="sub_req_id")
                G.add_node(child, type="verification_method")
                G.add_edge(parent, child)
            
        if include_docs:
            # method_id -> doc_id
            db.cursor.execute("""
                SELECT method_id, doc_id FROM V_join_documents
                WHERE method_id IS NOT NULL AND doc_id IS NOT NULL
            """)
            for parent, child in db.cursor.fetchall():
                G.add_node(parent, type="method_id")
                G.add_node(child, type="doc_id")
                G.add_edge(parent, child)
        
        # In build_graph(), after adding nodes:

        # Goals: store satisfaction_status
        db.cursor.execute("SELECT goal_id, satisfaction_status FROM goals")
        for gid, status in db.cursor.fetchall():
            if gid in G.nodes:
                G.nodes[gid]["status"] = status

        # Drone swarm requirements: store verification_status
        db.cursor.execute("SELECT swarm_req_id, verification_status FROM drone_swarm_requirements")
        for sid, status in db.cursor.fetchall():
            if sid in G.nodes:
                G.nodes[sid]["status"] = status

        # System requirements: store verification_status
        db.cursor.execute("SELECT sys_req_id, verification_status FROM system_requirements")
        for sid, status in db.cursor.fetchall():
            if sid in G.nodes:
                G.nodes[sid]["status"] = status

        # Subsystem requirements: store verification_status
        db.cursor.execute("SELECT sub_req_id, verification_status FROM subsystem_requirements")
        for sid, status in db.cursor.fetchall():
            if sid in G.nodes:
                G.nodes[sid]["status"] = status

    return G

def choose_node_type_and_id(G):
    """Ask user for node type using numbers and ID (or 'all') and optional depth cutoff."""
    node_types = ["goal_id", "swarm_req_id", "sys_req_id", "sub_req_id"]

    # Show numbered options
    print("Select node type to visualize from:")
    for i, t in enumerate(node_types, start=1):
        print(f"{i}: {t}")

    choice = input("Enter number corresponding to node type: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(node_types):
        raise ValueError(f"Invalid choice '{choice}'")

    node_type = node_types[int(choice) - 1]

    # Collect available nodes of this type
    candidates = [n for n, data in G.nodes(data=True) if data.get("type") == node_type]
    if not candidates:
        raise ValueError(f"No nodes found for type {node_type}")

    print(f"Available {node_type}s:", candidates)
    chosen_id = input(f"Enter {node_type} to visualize (or 'all'): ").strip()

    # Ask for max depth
    print("Select node type to visualize up to:")
    for i, t in enumerate(node_types, start=1):
        print(f"{i-1}: {t}")
    
    depth_choice = input("Enter number corresponding to node type: ").strip() #input("Enter max depth to expand (or press Enter for no limit): ").strip()
    max_depth = None
    if depth_choice.isdigit():
        max_depth = int(depth_choice)

    return node_type, chosen_id, candidates, max_depth

def plot_subgraph(G, root, save=False, h_padding=0.05, v_padding=0.05, max_depth=None):
    """
    Fully adaptive plotting of a hierarchy tree with optional depth cutoff.

    Parameters:
        G (nx.DiGraph): Full graph
        root (str|int): Root node ID
        save (bool): Save to file instead of show
        h_padding (float): Horizontal padding (0-0.5)
        v_padding (float): Vertical padding (0-0.5)
        max_depth (int|None): Maximum depth to expand children (None = no limit)
    """
    # Collect nodes up to max_depth
    sub_nodes = {root}
    frontier = [(root, 0)]  # (node, depth)

    while frontier:
        node, depth = frontier.pop()
        if max_depth is not None and depth >= max_depth:
            continue
        for child in G.successors(node):
            sub_nodes.add(child)
            frontier.append((child, depth + 1))

    # Build subgraph
    H = G.subgraph(sub_nodes).copy()

    # Compute tree depth (relative to H)
    def max_depth_calc(node, G):
        children = list(G.successors(node))
        if not children:
            return 1
        return 1 + max(max_depth_calc(child, G) for child in children)

    depth = max_depth_calc(root, H)
    num_nodes = len(H.nodes)

    # Dynamic figure size
    width = max(num_nodes / 2, 8) # Påverkar spacing mellan syskon
    height = max(depth * 1.5, 6) # Spelar ingen roll lol
    plt.figure(figsize=(width, height))

    # NODE SIZE AND FONT SIZE
    # Dynamic node and font size
    node_size = max(1500 - num_nodes * 20, 500) # Node size → change the 1500 (base size) and 500 (minimum size).
    font_size = max(9 - int(num_nodes / 50), 6) # Text size → change the formula or use a fixed value:

    # Horizontal layout width
    horiz_width = min(1.0, 0.5 + num_nodes / 50)
    adjusted_width = horiz_width * (1 - 2 * h_padding)
    xcenter = 0.5

    # Compute hierarchical positions
    # vert_gap → adds more space between parent and children
    # width passed to hierarchy_pos → spreads sibling nodes out more.
    pos = hierarchy_pos(H, root=root, vert_loc=1.0, vert_gap=0.02, width=adjusted_width * 10, xcenter=xcenter)

    # Apply horizontal padding
    for node in pos:
        pos[node] = (pos[node][0] * (1 - 2 * h_padding) + h_padding, pos[node][1])

    # Apply vertical padding
    y_values = [y for x, y in pos.values()]
    y_min, y_max = min(y_values), max(y_values)
    y_range = y_max - y_min if y_max != y_min else 1.0
    for node in pos:
        y = pos[node][1]
        pos[node] = (pos[node][0], v_padding + (y - y_min) / y_range * (1 - 2 * v_padding))

    # Build labels: show only ID
    labels = {n: str(n) for n in H.nodes}

    # Define a color map per node type depending on their verification status
    status_colors = {
        "goal_id": {
            "Satisfied": "green",
            "Not satisfied": "dimgrey",
            "Pending": "dimgrey"
        },
        "swarm_req_id": {
            "Verified": "mediumseagreen",
            "Failed": "red",
            "Inconclusive": "gray",
            "Pending": "gray"
        },
        "sys_req_id": {
            "Verified": "limegreen",
            "Failed": "red",
            "Inconclusive": "darkgrey",
            "Pending": "darkgrey"
        },
        "sub_req_id": {
            "Verified": "springgreen",
            "Failed": "red",
            "Inconclusive": "lightgrey",
            "Pending": "lightgrey"
        }
    }

    type_colors = {
        "goal_id": "dimgrey",
        "swarm_req_id": "gray",
        "sys_req_id": "darkgrey",
        "sub_req_id": "lightgrey",
        "verification_method": "blanchedalmond",
        "method_id": "blanchedalmond",
        "doc_id": "moccasin"
    }

    # Assign a color for each node in the subgraph
    node_colors = []
    for n in H.nodes:
        node_type = H.nodes[n].get("type")
        status = H.nodes[n].get("status")

        if node_type in status_colors and status in status_colors[node_type]:
            node_colors.append(status_colors[node_type][status])
        else:
            # fallback: type color (methods, docs, etc.)
            node_colors.append(type_colors.get(node_type, "lightgrey"))

    # Draw the tree with per-node colors
    nx.draw(
        H, pos, labels=labels,
        node_size=node_size, node_color=node_colors,
        font_size=font_size, font_weight="bold",
        arrowsize=15, edgecolors="black"
    )

    # Add legend
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(color="green", label="Goal Satisfied"),
        Patch(color="dimgrey", label="Goal Pending / not Satisfied"),

        Patch(color="mediumseagreen", label="Swarm_Req Verified"),
        Patch(color="gray", label="Swarm_Req Not Verified"),

        Patch(color="limegreen", label="Sys_Req Verified"),
        Patch(color="darkgrey", label="Sys_Req Not Verified"),

        Patch(color="springgreen", label="Sub_Req Verified"),
        Patch(color="lightgrey", label="Sub_Req Not Verified"),

        Patch(color="red", label="Failed Testing"),
        
        Patch(color="blanchedalmond", label="Verification Method"),
        Patch(color="moccasin", label="Document"),
    ]
    plt.legend(handles=legend_handles, loc="lower left", bbox_to_anchor=(1, 0))

    node_type = G.nodes[root].get("type", "unknown")
    title = f"Hierarchy starting from {node_type}: {root}"
    if max_depth is not None:
        title += f" (depth ≤ {max_depth})"
    plt.title(title, fontsize=14)

    if save:
        filename = f"{node_type}_{root}_depth{max_depth if max_depth else 'all'}.png".replace(":", "-")
        plt.savefig(filename, bbox_inches="tight")
        print(f"Saved: {filename}")
        plt.close()
    else:
        plt.show()

def run_tree_plot():
    """
    Launches the interactive plotting menu:
    asks for node type, ID, and depth, then plots.
    """
    # Ask user about including methods/docs
    include_methods = input("Include verification methods? (y/n): ").strip().lower() == "y"
    if include_methods:
        include_docs = input("Include documents? (y/n): ").strip().lower() == "y"
    else:
        include_docs = False

    G = build_graph(include_methods=include_methods, include_docs=include_docs)
    node_type, chosen_id, candidates, max_depth = choose_node_type_and_id(G)

    if chosen_id.lower() == "all":
        for root in candidates:
            plot_subgraph(G, root, save=True, max_depth=max_depth)
    else:
        if chosen_id not in candidates:
            raise ValueError(f"{chosen_id} not found in {node_type}s")
        plot_subgraph(G, chosen_id, save=False, max_depth=max_depth)
