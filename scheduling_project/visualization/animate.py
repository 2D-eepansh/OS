import matplotlib.pyplot as plt
import matplotlib.animation as animation

def show_gantt_chart(schedule, colors, title="CPU Scheduling Gantt Chart"):
    """
    Display a static Gantt chart
    """
    if not schedule:
        print("No schedule to display!")
        return
        
    fig, ax = plt.subplots(figsize=(12, 4))
    
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
        
        # Add text labels in the middle of each segment
        for start, width in segs:
            if width >= 0.8:
                ax.text(start + width/2, 0.5, proc,
                       ha='center', va='center', color='white', 
                       fontsize=12, fontweight='bold')
    
    # Formatting
    ax.set_xlim(-0.5, len(schedule) - 0.5)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("Time Units", fontsize=12)
    ax.set_ylabel("")
    ax.set_yticks([])
    
    # Add time markers and labels
    for i in range(len(schedule) + 1):
        ax.axvline(x=i-0.5, color='gray', linestyle='--', alpha=0.3)
    
    ax.set_xticks(range(len(schedule) + 1))
    ax.set_xticklabels([str(i) for i in range(len(schedule) + 1)])
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def animate(schedule, colors, interval=800):
    """
    Animate Gantt chart from schedule list
    """
    if not schedule:
        print("No schedule to animate!")
        return None
        
    fig, ax = plt.subplots(figsize=(10, 4))
    
    def update(frame):
        ax.clear()
        ax.set_xlim(-0.5, len(schedule) - 0.5)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel("Time Units")
        ax.set_ylabel("")
        ax.set_yticks([])
        
        # Add time markers
        for i in range(len(schedule)):
            ax.axvline(x=i-0.5, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(x=len(schedule)-0.5, color='gray', linestyle='--', alpha=0.3)
        
        # Build segments for each process up to current frame
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
        
        # Draw all segments
        for proc, segs in segments.items():
            color = colors.get(proc, 'gray')
            ax.broken_barh(segs, (0.1, 0.8), facecolors=color, edgecolors='black', linewidth=1)
            
            # Add text labels in the middle of each segment
            for start, width in segs:
                if width >= 0.8:  # Only add text if segment is wide enough
                    ax.text(start + width/2, 0.5, proc,
                           ha='center', va='center', color='white', 
                           fontsize=12, fontweight='bold')
        
        # Add time labels
        time_labels = [str(i) for i in range(frame + 2)]
        ax.set_xticks(range(-1, frame + 2))
        ax.set_xticklabels([''] + time_labels[:frame + 2])
        
        current_proc = schedule[frame] if frame < len(schedule) else "Complete"
        ax.set_title(f"CPU Scheduling Animation - Time: {frame} | Running: {current_proc}", 
                    fontsize=14, fontweight='bold')
        
        return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(schedule),
        interval=interval, repeat=False, blit=False
    )
    
    plt.tight_layout()
    plt.show()
    return ani
