import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm

# Set Times New Roman font with fallback
try:
    # Check if Times New Roman is available
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    if 'Times New Roman' in available_fonts:
        plt.rcParams['font.family'] = 'Times New Roman'
        print("Using Times New Roman font")
    else:
        # Fallback to serif fonts
        plt.rcParams['font.family'] = 'serif'
        print("Times New Roman not found, using default serif font")
except:
    plt.rcParams['font.family'] = 'serif'
    print("Using default serif font")

plt.rcParams['font.size'] = 12

def animate(schedule, processes, colors, interval=500):
    """
    Animate Gantt chart from schedule list
    processes = [(name, arrival, burst)]
    """
    if not schedule:
        print("No schedule to animate!")
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Add Idle color if not present
    if "Idle" in schedule and "Idle" not in colors:
        colors["Idle"] = "lightgray"

    # Compute completion times for metrics calculation
    completion_times = {}
    for name, at, bt in processes:
        completion_times[name] = 0
    
    def update(frame):
        ax.clear()
        
        # Set up the plot
        ax.set_xlim(-0.5, len(schedule) - 0.5)
        ax.set_ylim(-0.1, 2.5)
        ax.set_xlabel("Time (ms)", fontsize=12, fontweight='bold')
        ax.set_ylabel("")
        ax.set_yticks([])
        
        # Add time markers
        for i in range(len(schedule) + 1):
            ax.axvline(x=i-0.5, color='gray', linestyle='--', alpha=0.3)
        
        # Build segments up to current frame
        segments = {}
        for i in range(frame + 1):
            proc = schedule[i]
            if proc not in segments:
                segments[proc] = []
            
            # Check if this continues the last segment
            if segments[proc] and segments[proc][-1][0] + segments[proc][-1][1] == i:
                segments[proc][-1] = (segments[proc][-1][0], segments[proc][-1][1] + 1)
            else:
                segments[proc].append((i, 1))
            
            # Update completion time for non-idle processes
            if proc != "Idle" and proc in completion_times:
                completion_times[proc] = i + 1
        
        # Draw all segments
        for proc, segs in segments.items():
            color = colors.get(proc, 'gray')
            ax.broken_barh(segs, (0.1, 0.8), facecolors=color, edgecolors='black', linewidth=1)
            
            # Add text labels in segments
            for start, width in segs:
                if width >= 0.8:
                    ax.text(start + width/2, 0.5, proc,
                           ha='center', va='center', color='white', 
                           fontsize=11, fontweight='bold')
        
        # Add time labels
        ax.set_xticks(range(len(schedule) + 1))
        ax.set_xticklabels([str(i) for i in range(len(schedule) + 1)])
        
        # Display process metrics
        y_pos = 1.3
        ax.text(0, y_pos + 0.3, "Process Metrics:", fontsize=12, fontweight='bold', 
                color='darkblue')
        
        for name, at, bt in processes:
            ct = completion_times[name]
            tat = ct - at if ct > 0 else 0  # Turnaround Time
            wt = tat - bt if tat >= bt else 0  # Waiting Time
            
            metrics_text = f"{name}: CT={ct}, TAT={tat}, WT={wt}"
            ax.text(0, y_pos, metrics_text, fontsize=10, 
                   color='black')
            y_pos += 0.2
        
        # Current process info
        current_proc = schedule[frame] if frame < len(schedule) else "Complete"
        ax.set_title(f"FCFS Scheduling Animation - Time: {frame} ms | Running: {current_proc}", 
                    fontsize=14, fontweight='bold')
        
        return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(schedule),
        interval=interval, repeat=False, blit=False
    )
    
    plt.tight_layout()
    plt.show()
    return ani

def show_gantt_chart(schedule, processes, colors, title="FCFS Scheduling - Gantt Chart"):
    """
    Display a static Gantt chart with process metrics
    """
    if not schedule:
        print("No schedule to display!")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Add Idle color if not present
    if "Idle" in schedule and "Idle" not in colors:
        colors["Idle"] = "lightgray"
    
    # Build segments for each process
    segments = {}
    for i, proc in enumerate(schedule):
        if proc not in segments:
            segments[proc] = []
        
        # Check if this continues the last segment
        if segments[proc] and segments[proc][-1][0] + segments[proc][-1][1] == i:
            segments[proc][-1] = (segments[proc][-1][0], segments[proc][-1][1] + 1)
        else:
            segments[proc].append((i, 1))
    
    # Draw all segments
    for proc, segs in segments.items():
        color = colors.get(proc, 'gray')
        ax.broken_barh(segs, (0.1, 0.8), facecolors=color, edgecolors='black', linewidth=1)
        
        # Add text labels in segments
        for start, width in segs:
            if width >= 0.8:
                ax.text(start + width/2, 0.5, proc,
                       ha='center', va='center', color='white', 
                       fontsize=11, fontweight='bold')
    
    # Formatting
    ax.set_xlim(-0.5, len(schedule) - 0.5)
    ax.set_ylim(-0.1, 2.5)
    ax.set_xlabel("Time (ms)", fontsize=12, fontweight='bold')
    ax.set_ylabel("")
    ax.set_yticks([])
    
    # Add time markers and labels
    for i in range(len(schedule) + 1):
        ax.axvline(x=i-0.5, color='gray', linestyle='--', alpha=0.3)
    
    ax.set_xticks(range(len(schedule) + 1))
    ax.set_xticklabels([str(i) for i in range(len(schedule) + 1)])
    
    # Calculate and display final metrics
    completion_times = {}
    for i, proc in enumerate(schedule):
        if proc != "Idle":
            completion_times[proc] = i + 1
    
    # Display process metrics
    y_pos = 1.3
    ax.text(0, y_pos + 0.3, "Final Process Metrics:", fontsize=12, fontweight='bold', 
            color='darkblue')
    
    total_tat = 0
    total_wt = 0
    for name, at, bt in processes:
        ct = completion_times.get(name, 0)
        tat = ct - at if ct > 0 else 0
        wt = tat - bt if tat >= bt else 0
        total_tat += tat
        total_wt += wt
        
        metrics_text = f"{name}: CT={ct}, TAT={tat}, WT={wt}"
        ax.text(0, y_pos, metrics_text, fontsize=10, 
               color='black')
        y_pos += 0.2
    
    # Average metrics
    avg_tat = total_tat / len(processes)
    avg_wt = total_wt / len(processes)
    ax.text(0, y_pos + 0.1, f"Average TAT: {avg_tat:.2f}, Average WT: {avg_wt:.2f}", 
           fontsize=11, fontweight='bold', color='darkred')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
