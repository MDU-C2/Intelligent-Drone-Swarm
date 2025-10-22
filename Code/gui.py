# gui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpinBox, QLabel, QHBoxLayout
from threading import Thread
import main  # Import your main simulation file

class DroneControlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label + Spinbox for number of drones
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Number of Drones:"))
        self.drone_count = QSpinBox()
        self.drone_count.setRange(1, 50)
        self.drone_count.setValue(9)  # default
        h_layout.addWidget(self.drone_count)
        layout.addLayout(h_layout)

        # Run Simulation button
        self.sim_btn = QPushButton("Run Simulation")
        self.sim_btn.clicked.connect(self.run_simulation_with_count)
        layout.addWidget(self.sim_btn)

        # Start Search button
        self.start_btn = QPushButton("Start Search")
        self.start_btn.clicked.connect(main.start_search)
        layout.addWidget(self.start_btn)

        # Abort Mission button
        self.abort_btn = QPushButton("Abort Mission!")
        self.abort_btn.clicked.connect(main.abort_mission)
        layout.addWidget(self.abort_btn)

        self.setLayout(layout)
        self.setWindowTitle("Drone Swarm Control Panel")
        self.show()

    def run_simulation_with_count(self):
        """Reads number of drones from GUI and starts simulation"""
        num = self.drone_count.value()
        Thread(target=main.run_simulation, args=(num,)).start()
        print(f"Starting simulation with {num} drones...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DroneControlUI()
    sys.exit(app.exec_())
