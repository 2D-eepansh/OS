# 🖤 Modern FCFS CPU Scheduler - Professional Edition 🟡

A beautiful, modern CPU scheduling simulator with PyQt6 GUI featuring FCFS (First-Come, First-Served) algorithm with professional black & gold theme.

## ✨ Features

- **🎨 Modern PyQt6 GUI**: Professional black & gold themed interface
- **📊 Real-time Metrics**: Live calculation of CT, TAT, WT, and averages
- **🎬 Animated Visualization**: Smooth Gantt chart animation with progress tracking
- **🔧 Interactive Process Management**: Add/remove processes with validation
- **📈 Comprehensive Analytics**: Process status tracking and performance metrics
- **⚡ Professional Styling**: Dark theme with gold accents and modern typography

## 🏗️ Project Structure

```
scheduling_project/
│
├── gui/                     # Modern PyQt6 Interface
│   ├── __init__.py
│   └── main_window.py       # Main GUI application
│
├── algorithms/              # Scheduling Algorithms
│   ├── __init__.py
│   ├── fcfs.py             # FCFS implementation
│   ├── sjf.py              # Shortest Job First
│   ├── srtf.py             # Shortest Remaining Time First
│   ├── priority.py         # Priority Scheduling
│   └── round_robin.py      # Round Robin
│
├── visualization/           # Animation & Graphics
│   ├── __init__.py
│   └── animate.py          # Professional animations
│
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd scheduling_project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 🎯 Usage

### GUI Interface
1. **Add Processes**: Enter Process ID, Arrival Time, and Burst Time
2. **Minimum Requirement**: Add at least 2 processes (maximum 5)
3. **Run Animation**: Click "Run FCFS Animation" to see the scheduling
4. **View Metrics**: Real-time CT, TAT, WT calculations with status tracking

### Process Input Validation
- ✅ Process ID must be unique
- ✅ Arrival Time ≥ 0
- ✅ Burst Time > 0
- ✅ Maximum 5 processes allowed

### Metrics Displayed
- **CT (Completion Time)**: When process finishes execution
- **TAT (Turnaround Time)**: CT - Arrival Time
- **WT (Waiting Time)**: TAT - Burst Time
- **Average TAT & WT**: Overall system performance
- **Process Status**: Waiting ⏳, Running ⚡, Completed ✓

## 🎨 Theme & Design

- **Color Scheme**: Professional black (#1a1a1a) background with gold (#FFD700) accents
- **Typography**: Times New Roman font for professional appearance
- **Modern UI**: Native PyQt6 widgets with custom styling
- **Dark Mode**: Easy on the eyes with high contrast elements

## 🔧 Requirements

- **Python**: 3.7+
- **PyQt6**: 6.9.0+
- **matplotlib**: 3.5.0+
- **numpy**: 1.21.0+

## 🎬 Animation Features

- **Smooth Transitions**: Professional animation timing
- **Real-time Updates**: Live process metrics during execution
- **Progress Tracking**: Current time and completion status
- **Visual Feedback**: Color-coded process states
- **Professional Styling**: Dark theme matching the GUI

## 🚧 Future Enhancements

- **Export Results**: Save scheduling results to file
- **Algorithm Comparison**: Compare different scheduling algorithms
- **Process Configuration**: Save/load process sets
- **Advanced Metrics**: Response time, CPU utilization, throughput

---

**Created with ❤️ using PyQt6 and Python**