# CPU Scheduling Algorithms Simulator

This project implements various CPU scheduling algorithms with visualization capabilities.

## Features

- **First-Come, First-Served (FCFS)**: Non-preemptive scheduling algorithm
- **Shortest Job First (SJF)**: Non-preemptive scheduling based on burst time
- **Shortest Remaining Time First (SRTF)**: Preemptive version of SJF
- **Priority Scheduling**: Schedules processes based on priority
- **Round Robin**: Time-sharing algorithm with time quantum

## Project Structure

```
scheduling_project/
│
├── algorithms/
│   ├── __init__.py
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py
│   ├── priority.py
│   └── round_robin.py
│
├── visualization/
│   ├── __init__.py
│   └── animate.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone or download this project
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main application:
```
python main.py
```

## Requirements

- Python 3.7+
- matplotlib
- numpy