import numpy as np
from dataclasses import dataclass, field

@dataclass
class GridCell:
    """Represents one section of the search area."""
    id: int
    position: tuple
    assigned_drone: int = None
    searched: bool = False

class SearchArea:
    """Handles dividing the search area and managing grid assignments."""

    def __init__(self, grid_size=(3, 3), cell_size=1.5, home=(0, 0)):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.home = np.array(home)
        self.cells = self._generate_cells()

    def _generate_cells(self):
        """Create GridCell objects for each section in the search area."""
        rows, cols = self.grid_size
        cells = []
        cell_id = 0
        offset_x, offset_y = self.home  # shift the grid center
        for i in range(rows):
            for j in range(cols):
                x = (i - rows / 2) * self.cell_size + self.cell_size / 2 + offset_x
                y = (j - cols / 2) * self.cell_size + self.cell_size / 2 + offset_y
                cells.append(GridCell(id=cell_id, position=(x, y)))
                cell_id += 1
        return cells


    def reassign_cells_from_drone(self, failed_drone_id, new_drone_id):
        """
        Transfer all cells from a failed drone to another.
        """
        for cell in self.cells:
            if cell.assigned_drone == failed_drone_id and not cell.searched:
                cell.assigned_drone = new_drone_id

    def assign_drones(self, num_drones):
        """
        Assign cells so that each drone gets adjacent cells.
        """
        rows, cols = self.grid_size
        total_cells = rows * cols
        cells_per_drone = total_cells // num_drones
        extra = total_cells % num_drones

        drone_index = 0
        count = 0
        for r in range(rows):
            for c in range(cols):
                cell_id = r * cols + c
                cell = self.cells[cell_id]
                cell.assigned_drone = drone_index
                count += 1
                if (count >= cells_per_drone + (1 if extra > 0 else 0)) and drone_index < num_drones - 1:
                    count = 0
                    drone_index += 1
                    extra -= 1


    def mark_searched(self, cell_id):
        """Mark a specific grid cell as searched."""
        for cell in self.cells:
            if cell.id == cell_id:
                cell.searched = True
                return True
        return False

    def get_unsearched_cells(self, drone_id=None):
        """Return all unsearched cells (optionally filtered by assigned drone)."""
        if drone_id is not None:
            return [c for c in self.cells if not c.searched and c.assigned_drone == drone_id]
        return [c for c in self.cells if not c.searched]

    def get_cell_info(self):
        """Return a summary of all cells (for debugging or broadcast)."""
        return [
            {
                "id": c.id,
                "pos": c.position,
                "drone": c.assigned_drone,
                "searched": c.searched
            }
            for c in self.cells
        ]

    def __repr__(self):
        """Human-readable summary."""
        summary = "\n".join(
            [f"Cell {c.id}: Pos={c.position}, Drone={c.assigned_drone}, Searched={c.searched}"
             for c in self.cells]
        )
        return f"SearchArea({self.grid_size}, cell_size={self.cell_size}):\n" + summary
