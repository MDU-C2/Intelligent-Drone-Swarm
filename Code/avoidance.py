# avoidance.py
import numpy as np


def get_all_positions(env, num_drones):
    """Get all drone positions from environment."""
    return np.array([env._getDroneStateVector(i)[0:3] for i in range(num_drones)])


def avoidance_from_drones(my_pos, all_pos, my_idx,
                          radius=0.3, gain=1.0, max_push=1.0):
    """
    Repulsion force from nearby drones.
    Larger radius = earlier reaction.
    """
    push = np.zeros(3)
    for j, other_pos in enumerate(all_pos):
        if j == my_idx:
            continue
        diff = other_pos - my_pos
        dist = np.linalg.norm(diff[:2])
        if 1e-6 < dist < radius:
            direction = -diff / (dist + 1e-6)
            strength = gain * (1.0 / dist - 1.0 / radius) ** 2
            push += np.array([direction[0], direction[1], 0.0]) * strength
    n = np.linalg.norm(push)
    if n > max_push:
        push *= max_push / (n + 1e-9)
    return push


def avoidance_from_borders(my_pos, grid_size, cell_size, offset_xy,
                           margin=0.3, gain=0.6, max_push=0.6):
    """
    Repel drones from outside the white search area borders.
    grid_size = (rows, cols)
    offset_xy = (x, y) center of search area
    """
    rows, cols = grid_size
    half_x = cols * cell_size / 2.0
    half_y = rows * cell_size / 2.0
    cx, cy = offset_xy

    dx_left = (my_pos[0] - (cx - half_x)) - margin
    dx_right = (cx + half_x - my_pos[0]) - margin
    dy_bottom = (my_pos[1] - (cy - half_y)) - margin
    dy_top = (cy + half_y - my_pos[1]) - margin

    push = np.zeros(3)
    if dx_left < 0:
        push[0] += gain / (abs(dx_left) + 1e-3) ** 2
    if dx_right < 0:
        push[0] -= gain / (abs(dx_right) + 1e-3) ** 2
    if dy_bottom < 0:
        push[1] += gain / (abs(dy_bottom) + 1e-3) ** 2
    if dy_top < 0:
        push[1] -= gain / (abs(dy_top) + 1e-3) ** 2

    n = np.linalg.norm(push)
    if n > max_push:
        push *= max_push / (n + 1e-9)
    return push
