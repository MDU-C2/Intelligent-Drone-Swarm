# gui.py
import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, 
    QHBoxLayout, QSpinBox, QLabel, QTextEdit, QComboBox
)
from PyQt5.QtCore import QTimer
import controller
from gym_pybullet_drones.FLA402.tables import get_all_health_codes


class DroneControlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # --- Drone count control ---
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Number of Drones:"))
        self.drone_count = QSpinBox()
        self.drone_count.setRange(1, 50)
        self.drone_count.setValue(4)
        h_layout.addWidget(self.drone_count)
        layout.addLayout(h_layout)

        # --- Buttons ---
        self.sim_btn = QPushButton("Run Simulation")
        self.sim_btn.clicked.connect(self.run_simulation_with_count)
        layout.addWidget(self.sim_btn)

        self.start_btn = QPushButton("Start Search")
        self.start_btn.clicked.connect(controller.start_search)
        layout.addWidget(self.start_btn)

        self.abort_btn = QPushButton("Abort Mission!")
        self.abort_btn.clicked.connect(controller.abort_mission)
        layout.addWidget(self.abort_btn)

        # --- Text displays ---
        info_layout = QHBoxLayout()

        # Left column (broadcast)
        left_layout = QVBoxLayout()
        self.broadcast_label = QLabel("Drone Broadcast Information")
        self.broadcast_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #0080ff;")
        self.broadcast_display = QTextEdit()
        self.broadcast_display.setReadOnly(True)
        self.broadcast_display.setPlaceholderText("Drone Broadcast Information...")
        left_layout.addWidget(self.broadcast_label)
        left_layout.addWidget(self.broadcast_display)

        # Middle column: Health reports + fault injection controls
        middle_layout = QVBoxLayout()
        self.health_label = QLabel("Drone Health & Retasking")
        self.health_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #cc0000;")
        middle_layout.addWidget(self.health_label)

        # Text area for displaying alerts
        self.health_display = QTextEdit()
        self.health_display.setReadOnly(True)
        self.health_display.setPlaceholderText("Health alerts and retasking actions will appear here...")
        middle_layout.addWidget(self.health_display)

        # --- Fault Injection Controls ---
        inject_label = QLabel("Inject Drone Fault")
        inject_label.setStyleSheet("font-weight: bold; color: #444;")
        middle_layout.addWidget(inject_label)

        fault_row = QHBoxLayout()

        # Drone selector
        self.drone_selector = QComboBox()
        self.drone_selector.setToolTip("Select which drone to inject fault into")
        self.drone_selector.addItems([str(i) for i in range(0, 10)])  # Adjust max if needed
        fault_row.addWidget(QLabel("Drone ID:"))
        fault_row.addWidget(self.drone_selector)

        # Health selector (codes and names)
        self.health_selector = QComboBox()
        self.health_selector.setToolTip("Select fault/health condition")
        codes = get_all_health_codes()
        for code, name in codes.items():
            self.health_selector.addItem(f"{code} - {name}", code)
        fault_row.addWidget(QLabel("Health Code:"))
        fault_row.addWidget(self.health_selector)

        middle_layout.addLayout(fault_row)

        # Inject button
        self.inject_btn = QPushButton("Inject Fault")
        self.inject_btn.clicked.connect(self.send_health_status)
        middle_layout.addWidget(self.inject_btn)

        # Right column (assignments)
        right_layout = QVBoxLayout()
        self.assignment_label = QLabel("Drone–Section Assignments")
        self.assignment_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #0080ff;")
        self.assignment_display = QTextEdit()
        self.assignment_display.setReadOnly(True)
        self.assignment_display.setPlaceholderText("Drone Section Assignments...")
        right_layout.addWidget(self.assignment_label)
        right_layout.addWidget(self.assignment_display)

        info_layout.addLayout(left_layout)
        info_layout.addLayout(middle_layout)
        info_layout.addLayout(right_layout)
        layout.addLayout(info_layout)

        self.setLayout(layout)
        self.setWindowTitle("Drone Swarm Control Panel")

        # --- Timer to refresh info from controller ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_displays)
        self.timer.start(1000)  # update every 1 second

        self.show()

    def run_simulation_with_count(self):
        num = self.drone_count.value()
        threading.Thread(target=controller.run_simulation, args=(num,)).start()
        print(f"Starting simulation with {num} drones...")

    def update_displays(self):
        """Pull live text data from controller."""
        self.broadcast_display.setPlainText(controller.broadcast_text)
        self.assignment_display.setPlainText(controller.assignment_text)

        # Show latest health/retasking info
        if hasattr(controller, "middle_text"):
            current = self.health_display.toPlainText()
            new_msg = controller.middle_text
            if new_msg and (new_msg not in current):  # prevent duplicates
                self.health_display.append(new_msg)


    def send_health_status(self):
        """Send a fault injection command to the controller (and thus to test.py)."""
        import controller

        drone_id = int(self.drone_selector.currentText())
        # Get the selected code from the data role
        health_code = self.health_selector.currentData()
        controller.injected_fault = (drone_id, health_code)
        name = self.health_selector.currentText()
        print(f"[GUI] Injected fault {name} for Drone {drone_id}")
        self.health_display.append(f"[GUI] Injected fault {name} for Drone {drone_id}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DroneControlUI()
    sys.exit(app.exec_())
