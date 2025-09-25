# Shortest Remaining Time First (SRTF) scheduling algorithm

def srtf(processes):
    """
    Shortest Remaining Time First (Preemptive SJF)
    """
    schedule, time = [], 0
    processes = sorted(processes, key=lambda x: x[1])  # sort by arrival
    n = len(processes)
    remaining = {p[0]: p[2] for p in processes}  # burst times left
    ready, i = [], 0

    while i < n or ready:
        while i < n and processes[i][1] <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: remaining[x[0]])
            name, at, bt = ready[0]
            schedule.append(name)
            remaining[name] -= 1
            if remaining[name] == 0:
                ready.pop(0)
            time += 1
        else:
            time += 1
    return schedule
