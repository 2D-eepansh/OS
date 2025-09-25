from algorithms.fcfs import fcfs
from visualization.animate import animate, show_gantt_chart

def main():
    print("=" * 50)
    print("        FCFS SCHEDULING SIMULATOR")
    print("=" * 50)
    
    # Problem 42 Processes
    processes_fcfs = [("P1", 0, 3), ("P2", 1, 20), ("P3", 2, 2)]
    colors = {"P1": "tab:blue", "P2": "tab:green", "P3": "tab:orange", "Idle": "lightgray"}
    
    print("\nProcess Details:")
    print("Process | Arrival Time | Burst Time")
    print("-" * 35)
    for name, at, bt in processes_fcfs:
        print(f"  {name}    |      {at}       |     {bt}")
    
    # Generate schedule
    schedule = fcfs(processes_fcfs)
    print(f"\nGenerated Schedule: {schedule}")
    print(f"Total execution time: {len(schedule)} ms")
    
    print("\nVisualization Options:")
    print("1. Animated Gantt Chart")
    print("2. Static Gantt Chart")
    print("3. Both")
    
    choice = input("\nSelect option (1-3) or press Enter for animated: ").strip()
    
    if choice == '2':
        show_gantt_chart(schedule, processes_fcfs, colors)
    elif choice == '3':
        show_gantt_chart(schedule, processes_fcfs, colors)
        input("\nPress Enter to show animation...")
        animate(schedule, processes_fcfs, colors, interval=500)
    else:  # Default to animated
        animate(schedule, processes_fcfs, colors, interval=500)

if __name__ == "__main__":
    main()
