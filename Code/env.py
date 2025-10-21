import numpy as np
import pybullet as p
import pybullet_data

from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary

#grid_size = (10, 10)
#cell_size = 1.0

class SearchAreaAviary(CtrlAviary):

    def __init__(self,
                 grid_size=(10, 10),
                 cell_size=1.0,
                 home_position=(0, 0),
                 *args, **kwargs):
        """
        grid_size : tuple(int, int)
            Number of grid cells along X and Y.
        cell_size : float
            Size (meters) of each grid square.
        home_position : tuple(float, float)
            The XY position of the home/start point.
        """
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.home_position = home_position

        super().__init__(*args, **kwargs)

        self._create_green_ground()
        self._create_grid_lines()
        self._create_helipad(self.home_position)

    def _create_green_ground(self):
        """Loads and colors the ground plane green."""
        p.resetBasePositionAndOrientation(self.PLANE_ID, [0, 0, 0], [0, 0, 0, 1], physicsClientId=self.CLIENT)
        p.changeVisualShape(self.PLANE_ID, -1, rgbaColor=[0, 1, 0, 1], physicsClientId=self.CLIENT)

    def get_grid_cell_centers(grid_size, cell_size):
        centers = []
        width_x, width_y = grid_size
        for gx in range(width_x):
            for gy in range(width_y):
                x = (gx - width_x / 2) * cell_size + cell_size / 2
                y = (gy - width_y / 2) * cell_size + cell_size / 2
                centers.append((x,y))
        return np.array(centers)

    def _create_grid_lines(self):
        """Draws white grid lines on the green ground to show search squares."""
        width_x, width_y = self.grid_size
        half_x = width_x * self.cell_size / 2
        half_y = width_y * self.cell_size / 2
        
    def _create_helipad(self, position=(0, 0, 0)):
        """Creates a simple circular helipad marker."""

        radius = 0.6
        height = 0.02
        base_color = [0.2, 0.2, 0.2, 1]  # dark gray pad
        border_color = [1, 1, 1, 1]      # white border

        # Main pad surface
        pad_visual = p.createVisualShape(
            shapeType=p.GEOM_CYLINDER,
            radius=radius,
            length=height,
            rgbaColor=base_color,
            physicsClientId=self.CLIENT
        )

        # Spawn the helipad
        p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=pad_visual,
            basePosition=[*position, 0.01],
            physicsClientId=self.CLIENT
        )

        # Draw circular border
        for angle in range(0, 360, 10):
            a1 = np.radians(angle)
            a2 = np.radians(angle + 10)
            p.addUserDebugLine(
                [position[0] + radius * np.cos(a1), position[1] + radius * np.sin(a1), 0.02],
                [position[0] + radius * np.cos(a2), position[1] + radius * np.sin(a2), 0.02],
                border_color, 2, 0, physicsClientId=self.CLIENT
            )

        # Add white "H" text
        p.addUserDebugText(
            "H",
            [position[0] - 0.15, position[1] - 0.2, 0.05],
            textColorRGB=[1, 1, 1],
            textSize=2,
            lifeTime=0,
            physicsClientId=self.CLIENT
        )

