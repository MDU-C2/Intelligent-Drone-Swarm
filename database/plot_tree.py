# plot_tree.py

import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

from connect_database import connect_database
from create_tables import create_tables

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

def build_graph():
    """Builds the full directed graph from database relationships with type info."""
    G = nx.DiGraph()

    with connect_database("test.db") as db:
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

        # # sys_req -> sub_req
        # db.cursor.execute("""
        #     SELECT sys_req_id, sub_req_id FROM sysreq_children
        #     WHERE sys_req_id IS NOT NULL AND sub_req_id IS NOT NULL
        # """)
        # for parent, child in db.cursor.fetchall():
        #     G.add_node(parent, type="sys_req_id")
        #     G.add_node(child, type="sub_req_id")
        #     G.add_edge(parent, child)
    return G

def choose_node_type_and_id(G):
    """Ask user for node type using numbers and ID (or 'all')."""
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

    return node_type, chosen_id, candidates

def plot_subgraph(G, root, save=False, h_padding=0.05, v_padding=0.05):
    """
    Fully adaptive plotting of a hierarchy tree.
    """
    descendants = nx.descendants(G, root)
    sub_nodes = {root} | descendants
    H = G.subgraph(sub_nodes).copy()

    # Compute tree depth
    def max_depth(node, G):
        children = list(G.successors(node))
        if not children:
            return 1
        return 1 + max(max_depth(child, G) for child in children)

    depth = max_depth(root, H)
    num_nodes = len(H.nodes)

    # Dynamic figure size
    width = max(num_nodes / 2, 8)
    height = max(depth * 1.5, 6)
    plt.figure(figsize=(width, height))

    # Dynamic node and font size
    node_size = max(2000 - num_nodes * 20, 500)
    font_size = max(9 - int(num_nodes / 50), 6)

    # Horizontal layout width
    horiz_width = min(1.0, 0.5 + num_nodes / 50)
    adjusted_width = horiz_width * (1 - 2 * h_padding)
    xcenter = 0.5

    # Compute hierarchical positions
    pos = hierarchy_pos(H, root=root, vert_loc=1.0, vert_gap=0.15,
                        width=adjusted_width, xcenter=xcenter)

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

    # Draw the tree
    nx.draw(H, pos, with_labels=True,
            node_size=node_size, node_color="lightgreen",
            font_size=font_size, font_weight="bold",
            arrowsize=15, edgecolors="black")

    node_type = G.nodes[root].get("type", "unknown")
    plt.title(f"Hierarchy starting from {node_type}: {root}", fontsize=14)

    if save:
        filename = f"{node_type}_{root}.png".replace(":", "-")
        plt.savefig(filename, bbox_inches="tight")
        print(f"✅ Saved: {filename}")
        plt.close()
    else:
        plt.show()

#if __name__ == "__main__":
def run_tree_plot():
    """
    Launches the interactive plotting menu:
    asks for node type and ID, then plots.
    """
    G = build_graph()
    node_type, chosen_id, candidates = choose_node_type_and_id(G)

    if chosen_id.lower() == "all":
        for root in candidates:
            plot_subgraph(G, root, save=True)
    else:
        if chosen_id not in candidates:
            raise ValueError(f"{chosen_id} not found in {node_type}s")
        plot_subgraph(G, chosen_id, save=False)
