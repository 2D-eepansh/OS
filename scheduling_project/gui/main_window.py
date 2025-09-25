"""
Modern PyQt6 GUI for CPU Scheduling with Black & Gold Theme
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QGroupBox, QFrame, QMessageBox, QSpacerItem, 
                            QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPainter, QColor

class ModernSchedulerGUI(QMainWindow):
    """Main window for the CPU Scheduler with modern black & gold theme"""
    
    # Signal for running animation
    run_animation_signal = pyqtSignal(list, dict)
    
    def __init__(self):
        super().__init__()
        self.processes = []  # List of (id, arrival, burst) tuples
        self.max_processes = 5
        self.min_processes = 2
        self.animation = None  # Keep reference to animation
        
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🖤 FCFS CPU Scheduler - Professional Edition 🟡")
        self.setGeometry(100, 100, 800, 700)
        self.setMinimumSize(750, 650)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.create_title(main_layout)
        
        # Process input section
        self.create_input_section(main_layout)
        
        # Process table section
        self.create_table_section(main_layout)
        
        # Control buttons
        self.create_control_section(main_layout)
        
        # Status bar
        self.create_status_section(main_layout)
    
    def create_title(self, layout):
        """Create the title section"""
        title_frame = QFrame()
        title_frame.setFrameStyle(QFrame.Shape.Box)
        title_layout = QVBoxLayout(title_frame)
        
        title = QLabel("FCFS CPU Scheduler")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #FFD700;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d2d2d, stop:0.5 #1a1a1a, stop:1 #2d2d2d);
                border-radius: 10px;
            }
        """)
        
        subtitle = QLabel("Professional Process Scheduling Simulator")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #cccccc;
                padding: 5px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addWidget(title_frame)
    
    def create_input_section(self, layout):
        """Create the process input section"""
        input_group = QGroupBox("Process Input")
        input_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #FFD700;
                border: 2px solid #FFD700;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        input_layout = QGridLayout(input_group)
        input_layout.setSpacing(15)
        
        # Process ID input
        pid_label = QLabel("Process ID:")
        pid_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("e.g., P1, P2, P3...")
        
        # Arrival Time input
        at_label = QLabel("Arrival Time:")
        at_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.at_input = QLineEdit()
        self.at_input.setPlaceholderText("0, 1, 2...")
        
        # Burst Time input
        bt_label = QLabel("Burst Time:")
        bt_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.bt_input = QLineEdit()
        self.bt_input.setPlaceholderText("1, 2, 3...")
        
        # Add process button
        self.add_btn = QPushButton("➕ Add Process")
        self.add_btn.clicked.connect(self.add_process)
        
        # Remove process button
        self.remove_btn = QPushButton("🗑️ Remove Last")
        self.remove_btn.clicked.connect(self.remove_process)
        self.remove_btn.setEnabled(False)
        
        # Layout the input fields
        input_layout.addWidget(pid_label, 0, 0)
        input_layout.addWidget(self.pid_input, 0, 1)
        input_layout.addWidget(at_label, 0, 2)
        input_layout.addWidget(self.at_input, 0, 3)
        input_layout.addWidget(bt_label, 0, 4)
        input_layout.addWidget(self.bt_input, 0, 5)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.remove_btn)
        button_layout.addStretch()
        
        input_layout.addLayout(button_layout, 1, 0, 1, 6)
        
        layout.addWidget(input_group)
    
    def create_table_section(self, layout):
        """Create the process table section"""
        table_group = QGroupBox("Current Processes")
        table_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #FFD700;
                border: 2px solid #FFD700;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        table_layout = QVBoxLayout(table_group)
        
        # Process count label
        self.count_label = QLabel("Processes: 0/5 (Minimum 2 required)")
        self.count_label.setStyleSheet("color: #cccccc; font-size: 12px; padding: 5px;")
        table_layout.addWidget(self.count_label)
        
        # Process table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["Process ID", "Arrival Time", "Burst Time", "Status"])
        
        # Style the table
        self.process_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: white;
                gridline-color: #FFD700;
                border: 1px solid #FFD700;
                selection-background-color: #FFD700;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #FFD700;
                font-weight: bold;
                border: 1px solid #FFD700;
                padding: 8px;
            }
        """)
        
        table_layout.addWidget(self.process_table)
        layout.addWidget(table_group)
    
    def create_control_section(self, layout):
        """Create the control buttons section"""
        control_layout = QHBoxLayout()
        
        # Run Animation button
        self.run_btn = QPushButton("🎬 Run FCFS Animation")
        self.run_btn.clicked.connect(self.run_animation)
        self.run_btn.setEnabled(False)
        self.run_btn.setMinimumHeight(50)
        
        # Clear All button
        self.clear_btn = QPushButton("🧹 Clear All Processes")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setMinimumHeight(50)
        
        control_layout.addWidget(self.run_btn)
        control_layout.addWidget(self.clear_btn)
        
        layout.addLayout(control_layout)
    
    def create_status_section(self, layout):
        """Create the status section"""
        self.status_label = QLabel("Ready to add processes. Add at least 2 processes to start scheduling.")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 10px;
                background-color: #2d2d2d;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.status_label)
    
    def apply_theme(self):
        """Apply the black & gold theme to the entire application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: white;
            }
            
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #555555;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border: 2px solid #FFD700;
            }
            
            QPushButton {
                background-color: #2d2d2d;
                color: #FFD700;
                border: 2px solid #FFD700;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            
            QPushButton:hover {
                background-color: #FFD700;
                color: #1a1a1a;
            }
            
            QPushButton:pressed {
                background-color: #FFA500;
            }
            
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
                border: 2px solid #555555;
            }
        """)
    
    def add_process(self):
        """Add a new process to the list"""
        pid = self.pid_input.text().strip()
        at_text = self.at_input.text().strip()
        bt_text = self.bt_input.text().strip()
        
        # Validation
        if not pid or not at_text or not bt_text:
            self.show_error("Please fill all fields!")
            return
        
        if len(self.processes) >= self.max_processes:
            self.show_error(f"Maximum {self.max_processes} processes allowed!")
            return
        
        # Check if process ID already exists
        if any(p[0] == pid for p in self.processes):
            self.show_error(f"Process {pid} already exists!")
            return
        
        try:
            at = int(at_text)
            bt = int(bt_text)
            if at < 0 or bt <= 0:
                raise ValueError("Invalid times")
        except ValueError:
            self.show_error("Arrival time must be ≥ 0 and burst time must be > 0!")
            return
        
        # Add process
        self.processes.append((pid, at, bt))
        self.update_table()
        self.clear_inputs()
        self.update_status()
    
    def remove_process(self):
        """Remove the last process"""
        if self.processes:
            self.processes.pop()
            self.update_table()
            self.update_status()
    
    def clear_all(self):
        """Clear all processes"""
        self.processes.clear()
        self.update_table()
        self.update_status()
    
    def update_table(self):
        """Update the process table"""
        self.process_table.setRowCount(len(self.processes))
        
        for i, (pid, at, bt) in enumerate(self.processes):
            self.process_table.setItem(i, 0, QTableWidgetItem(pid))
            self.process_table.setItem(i, 1, QTableWidgetItem(str(at)))
            self.process_table.setItem(i, 2, QTableWidgetItem(str(bt)))
            self.process_table.setItem(i, 3, QTableWidgetItem("Ready"))
        
        # Resize columns
        self.process_table.resizeColumnsToContents()
    
    def update_status(self):
        """Update the status and button states"""
        count = len(self.processes)
        self.count_label.setText(f"Processes: {count}/{self.max_processes} (Minimum {self.min_processes} required)")
        
        # Update button states
        self.remove_btn.setEnabled(count > 0)
        self.clear_btn.setEnabled(count > 0)
        self.run_btn.setEnabled(count >= self.min_processes)
        
        # Update status message
        if count == 0:
            self.status_label.setText("Ready to add processes. Add at least 2 processes to start scheduling.")
        elif count < self.min_processes:
            self.status_label.setText(f"Add {self.min_processes - count} more process(es) to run the animation.")
        else:
            self.status_label.setText(f"Ready to run! Click 'Run FCFS Animation' to see the scheduling.")
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.pid_input.clear()
        self.at_input.clear()
        self.bt_input.clear()
        self.pid_input.setFocus()
    
    def show_error(self, message):
        """Show error message"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Input Error")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #FFD700;
                color: black;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
        """)
        msg.exec()
    
    def run_animation(self):
        """Run the FCFS animation"""
        if len(self.processes) < self.min_processes:
            self.show_error(f"Need at least {self.min_processes} processes!")
            return
        
        # Import and run the animation
        from algorithms.fcfs import fcfs
        from visualization.animate import animate
        
        # Convert processes for algorithm
        processes_for_algo = [(pid, at, bt) for pid, at, bt in self.processes]
        
        # Professional color scheme matching the GUI theme
        colors = {}
        # Elegant colors that complement the black & gold theme
        color_list = [
            "#FFD700",  # Gold - primary accent
            "#87CEEB",  # Sky Blue - cool complement
            "#98FB98",  # Pale Green - success color
            "#DDA0DD",  # Plum - elegant purple
            "#F0E68C"   # Khaki - warm neutral
        ]
        for i, (pid, _, _) in enumerate(self.processes):
            colors[pid] = color_list[i % len(color_list)]
        colors["Idle"] = "#404040"  # Darker gray for idle periods
        
        # Generate schedule
        schedule = fcfs(processes_for_algo)
        
        # Run animation and keep reference
        self.status_label.setText("Running FCFS animation...")
        try:
            self.animation = animate(schedule, processes_for_algo, colors, interval=800)
            self.status_label.setText("Animation complete! Add more processes or clear to start over.")
        except Exception as e:
            self.show_error(f"Animation error: {str(e)}")
            self.status_label.setText("Animation failed. Please try again.")


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Set application properties
    app.setApplicationName("FCFS CPU Scheduler")
    app.setApplicationVersion("2.0")
    
    # Create and show the main window
    window = ModernSchedulerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()