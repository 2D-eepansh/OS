# Round Robin scheduling algorithm

from collections import deque

def round_robin(processes, quantum=2):
    """
    Round Robin Scheduling
    processes = [(name, arrival, burst)]
    """
    time, schedule = 0, []
    processes = sorted(processes, key=lambda x: x[1])
    queue = deque()
    remaining = {p[0]: p[2] for p in processes}
    i, n = 0, len(processes)

    while i < n or queue:
        while i < n and processes[i][1] <= time:
            queue.append(processes[i][0])
            i += 1
        if queue:
            name = queue.popleft()
            run_time = min(quantum, remaining[name])
            schedule.extend([name] * run_time)
            time += run_time
            remaining[name] -= run_time
            while i < n and processes[i][1] <= time:
                queue.append(processes[i][0])
                i += 1
            if remaining[name] > 0:
                queue.append(name)
        else:
            time += 1
    return schedule
