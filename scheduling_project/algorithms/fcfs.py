# First-Come, First-Served (FCFS) scheduling algorithm

def fcfs(processes):
    """
    First Come First Serve Scheduling
    processes = [(name, arrival, burst)]
    Returns: schedule list of process names per time unit
    """
    schedule = []
    time = 0
    for name, at, bt in processes:
        if time < at:
            time = at
        schedule.extend([name] * bt)
        time += bt
    return schedule
