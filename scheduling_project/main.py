# Main entry point for the CPU scheduling project

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin
from visualization.animate import animate, show_gantt_chart

# Example processes
processes_fcfs = [("P1", 0, 4), ("P2", 1, 3), ("P3", 2, 2)]
processes_priority = [("P1", 0, 4, 2), ("P2", 1, 3, 1), ("P3", 2, 2, 3)]

colors = {"P1": "tab:blue", "P2": "tab:green", "P3": "tab:orange"}

def main():
    print("CPU Scheduling Algorithms Simulator")
    print("=" * 40)
    
    algorithms = {
        '1': ('First-Come First-Served (FCFS)', lambda: fcfs(processes_fcfs)),
        '2': ('Shortest Job First (SJF)', lambda: sjf(processes_fcfs)),
        '3': ('Shortest Remaining Time First (SRTF)', lambda: srtf(processes_fcfs)),
        '4': ('Priority Scheduling', lambda: priority_scheduling(processes_priority)),
        '5': ('Round Robin (quantum=2)', lambda: round_robin(processes_fcfs, quantum=2))
    }
    
    print("\nAvailable Algorithms:")
    for key, (name, _) in algorithms.items():
        print(f"{key}. {name}")
    
    choice = input("\nSelect algorithm (1-5) or press Enter for Round Robin: ").strip()
    if not choice:
        choice = '5'
    
    if choice in algorithms:
        algo_name, algo_func = algorithms[choice]
        print(f"\nRunning {algo_name}...")
        
        # Show process details
        if choice == '4':  # Priority scheduling
            print("Processes: (Name, Arrival, Burst, Priority)")
            for p in processes_priority:
                print(f"  {p}")
        else:
            print("Processes: (Name, Arrival, Burst)")
            for p in processes_fcfs:
                print(f"  {p}")
        
        schedule = algo_func()
        print(f"\nSchedule: {schedule}")
        print(f"Total time: {len(schedule)} units")
        
        # Show options for visualization
        viz_choice = input("\nVisualization options:\n1. Animated\n2. Static Gantt Chart\n3. Both\nChoice (1-3) or Enter for animated: ").strip()
        
        if viz_choice == '2':
            show_gantt_chart(schedule, colors, f"{algo_name} - Gantt Chart")
        elif viz_choice == '3':
            show_gantt_chart(schedule, colors, f"{algo_name} - Gantt Chart")
            animate(schedule, colors)
        else:  # Default to animated
            animate(schedule, colors)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
