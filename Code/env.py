import numpy as np
import pybullet as p
import pybullet_data

from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary

#grid_size = (10, 10)
#section_size = 1.0

class SearchAreaAviary(CtrlAviary):
    def __init__(self,
                 grid_size=(10, 10),
                 section_size=1.0,
                 home_position=(0, 0),
                 search_area_offset=(5, 0),
                 helipad_radius=0.6,
                 *args, **kwargs):
        
        self.grid_size = grid_size
        self.section_size = section_size
        self.home_position = home_position
        self.search_area_offset = search_area_offset
        self.helipad_radius = helipad_radius 

        super().__init__(*args, **kwargs)

        self._create_green_ground()
        self._create_search_area_overlay()
        self._create_grid_lines()
        self._create_helipad(self.home_position)



    def _create_green_ground(self):
        """Loads and colors the ground plane green."""
        p.resetBasePositionAndOrientation(self.PLANE_ID, [0, 0, 0], [0, 0, 0, 1], physicsClientId=self.CLIENT)
        p.changeVisualShape(self.PLANE_ID, -1, rgbaColor=[0, 1, 0, 1], physicsClientId=self.CLIENT)

    def _create_search_area_overlay(self):
        """Creates a white rectangular area overlay within the green ground."""
        width_x, width_y = self.grid_size
        half_x = width_x * self.section_size / 2
        half_y = width_y * self.section_size / 2

        # Compute where to place the search area
        center_x = self.home_position[0] + self.search_area_offset[0]
        center_y = self.home_position[1] + self.search_area_offset[1]

        overlay_visual = p.createVisualShape(
            shapeType=p.GEOM_BOX,
            halfExtents=[half_x, half_y, 0.001],
            rgbaColor=[1, 1, 1, 1],
            physicsClientId=self.CLIENT
        )

        p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=overlay_visual,
            basePosition=[center_x, center_y, 0.001],
            physicsClientId=self.CLIENT
        )

        # Optional: black outline
        for x in [-half_x, half_x]:
            p.addUserDebugLine(
                [center_x + x, center_y - half_y, 0.02],
                [center_x + x, center_y + half_y, 0.02],
                [0, 0, 0], 2, 0, physicsClientId=self.CLIENT
            )
        for y in [-half_y, half_y]:
            p.addUserDebugLine(
                [center_x - half_x, center_y + y, 0.02],
                [center_x + half_x, center_y + y, 0.02],
                [0, 0, 0], 2, 0, physicsClientId=self.CLIENT
            )
            # --- Add grid lines to show sections clearly ---
        rows, cols = self.grid_size

        # Draw vertical grid lines
        for i in range(1, cols):
            x = center_x - half_x + i * self.section_size
            p.addUserDebugLine(
                [x, center_y - half_y, 0.021],
                [x, center_y + half_y, 0.021],
                [0, 0, 0], 2, 0, physicsClientId=self.CLIENT
            )

        # Draw horizontal grid lines
        for j in range(1, rows):
            y = center_y - half_y + j * self.section_size
            p.addUserDebugLine(
                [center_x - half_x, y, 0.021],
                [center_x + half_x, y, 0.021],
                [0, 0, 0], 2, 0, physicsClientId=self.CLIENT
            )

        # Optional: label each cell in the grid
        cell_id = 0
        for i in range(rows):
            for j in range(cols):
                cell_x = center_x - half_x + (i + 0.5) * self.section_size
                cell_y = center_y - half_y + (j + 0.5) * self.section_size
                p.addUserDebugText(
                    str(cell_id),
                    [cell_x, cell_y, 0.05],
                    textColorRGB=[0, 0, 0],
                    textSize=1.5,
                    lifeTime=0,
                    physicsClientId=self.CLIENT
                )
                cell_id += 1


    def get_grid_cell_centers(grid_size, section_size):
        centers = []
        width_x, width_y = grid_size
        for gx in range(width_x):
            for gy in range(width_y):
                x = (gx - width_x / 2) * section_size + section_size / 2
                y = (gy - width_y / 2) * section_size + section_size / 2
                centers.append((x,y))
        return np.array(centers)

    def _create_grid_lines(self):
        """Draws white grid lines on the green ground to show search squares."""
        width_x, width_y = self.grid_size
        half_x = width_x * self.section_size / 2
        half_y = width_y * self.section_size / 2
        
    def _create_helipad(self, position=(0, 0, 0)):
        """Creates a circular helipad that scales with swarm size."""
        # Increase size multiplier for stronger visual effect
        radius = max(0.6, self.helipad_radius * 1.2)
        print(f"[ENV] Creating helipad with visual radius = {radius:.2f} (helipad_radius={self.helipad_radius:.2f})")

        height = 0.02
        base_color = [0.2, 0.2, 0.2, 1]
        border_color = [1, 1, 1, 1]

        pad_visual = p.createVisualShape(
            shapeType=p.GEOM_CYLINDER,
            radius=radius,
            length=height,
            rgbaColor=base_color,
            physicsClientId=self.CLIENT
        )

        p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=pad_visual,
            basePosition=[*position, 0.01],
            physicsClientId=self.CLIENT
        )

        for angle in range(0, 360, 10):
            a1 = np.radians(angle)
            a2 = np.radians(angle + 10)
            p.addUserDebugLine(
                [position[0] + radius * np.cos(a1), position[1] + radius * np.sin(a1), 0.02],
                [position[0] + radius * np.cos(a2), position[1] + radius * np.sin(a2), 0.02],
                border_color, 2, 0, physicsClientId=self.CLIENT
            )

        # Scale text size proportionally
        p.addUserDebugText(
            "H",
            [position[0] - 0.3 * radius, position[1] - 0.3 * radius, 0.05],
            textColorRGB=[1, 1, 1],
            textSize=max(2, radius * 1.2),
            lifeTime=0,
            physicsClientId=self.CLIENT
        )
    
    def mark_section_as_searched(self, cell_center, color=(0, 1, 0)):
        """
        Overlays a green box at the given cell center to indicate it has been searched.
        """
        x, y = cell_center
        half_extent = self.section_size / 2.0 * 0.95  # slightly smaller to fit within grid lines

        visual_shape = p.createVisualShape(
            shapeType=p.GEOM_BOX,
            halfExtents=[half_extent, half_extent, 0.001],
            rgbaColor=[color[0], color[1], color[2], 0.6],  # semi-transparent green
            physicsClientId=self.CLIENT
        )

        p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=visual_shape,
            basePosition=[x, y, 0.002],  # slightly above the white area
            physicsClientId=self.CLIENT
        )




