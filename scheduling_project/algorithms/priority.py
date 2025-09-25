# Priority scheduling algorithm

def priority_scheduling(processes):
    """
    Non-preemptive Priority Scheduling
    processes = [(name, arrival, burst, priority)]
    Lower priority number = higher priority
    """
    processes = sorted(processes, key=lambda x: (x[1], x[3]))
    schedule, time = [], 0
    ready = []
    i = 0
    n = len(processes)

    while i < n or ready:
        while i < n and processes[i][1] <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x[3])  # pick highest priority
            name, at, bt, pr = ready.pop(0)
            schedule.extend([name] * bt)
            time += bt
        else:
            time += 1
    return schedule
