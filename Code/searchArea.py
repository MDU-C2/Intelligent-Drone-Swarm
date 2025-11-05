import numpy as np
from dataclasses import dataclass, field

@dataclass
class Gridsection:
    """Represents one section of the search area."""
    id: int
    position: tuple
    assigned_drone: int = None
    searched: bool = False

class SearchArea:
    """Handles dividing the search area and managing grid assignments."""

    def __init__(self, grid_size=(3, 3), section_size=1.5, home=(0, 0)):
        self.grid_size = grid_size
        self.section_size = section_size
        self.home = np.array(home)
        self.sections = self._generate_sections()

    def _generate_sections(self):
        """Create Gridsection objects for each section in the search area."""
        rows, cols = self.grid_size
        sections = []
        section_id = 0
        offset_x, offset_y = self.home  # shift the grid center
        for i in range(rows):
            for j in range(cols):
                x = (i - rows / 2) * self.section_size + self.section_size / 2 + offset_x
                y = (j - cols / 2) * self.section_size + self.section_size / 2 + offset_y
                sections.append(Gridsection(id=section_id, position=(x, y)))
                section_id += 1
        return sections


    def reassign_sections_from_drone(self, failed_drone_id, new_drone_id):
        """
        Transfer all sections from a failed drone to another.
        """
        for section in self.sections:
            if section.assigned_drone == failed_drone_id and not section.searched:
                section.assigned_drone = new_drone_id

    def assign_drones(self, num_drones):
        """
        Assign sections so that each drone gets adjacent sections.
        """
        rows, cols = self.grid_size
        total_sections = rows * cols
        sections_per_drone = total_sections // num_drones
        extra = total_sections % num_drones

        drone_index = 0
        count = 0
        for r in range(rows):
            for c in range(cols):
                section_id = r * cols + c
                section = self.sections[section_id]
                section.assigned_drone = drone_index
                count += 1
                if (count >= sections_per_drone + (1 if extra > 0 else 0)) and drone_index < num_drones - 1:
                    count = 0
                    drone_index += 1
                    extra -= 1


    def mark_searched(self, section_id):
        """Mark a specific grid section as searched."""
        for section in self.sections:
            if section.id == section_id:
                section.searched = True
                return True
        return False

    def get_unsearched_sections(self, drone_id=None):
        """Return all unsearched sections (optionally filtered by assigned drone)."""
        if drone_id is not None:
            return [c for c in self.sections if not c.searched and c.assigned_drone == drone_id]
        return [c for c in self.sections if not c.searched]

    def get_section_info(self):
        """Return a summary of all sections (for debugging or broadcast)."""
        return [
            {
                "id": c.id,
                "pos": c.position,
                "drone": c.assigned_drone,
                "searched": c.searched
            }
            for c in self.sections
        ]

    def __repr__(self):
        """Human-readable summary."""
        summary = "\n".join(
            [f"section {c.id}: Pos={c.position}, Drone={c.assigned_drone}, Searched={c.searched}"
             for c in self.sections]
        )
        return f"SearchArea({self.grid_size}, section_size={self.section_size}):\n" + summary
