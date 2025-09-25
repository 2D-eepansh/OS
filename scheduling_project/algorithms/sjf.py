# Shortest Job First (SJF) scheduling algorithm

def sjf(processes):
    """
    Shortest Job First (Non-preemptive)
    """
    processes = sorted(processes, key=lambda x: (x[1], x[2]))  # sort by arrival, then burst
    schedule, time = [], 0
    ready = []
    i = 0
    n = len(processes)

    while i < n or ready:
        while i < n and processes[i][1] <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x[2])  # pick shortest burst
            name, at, bt = ready.pop(0)
            schedule.extend([name] * bt)
            time += bt
        else:
            time += 1
    return schedule
