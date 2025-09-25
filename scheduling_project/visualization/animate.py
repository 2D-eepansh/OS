import matplotlib
matplotlib.use('Qt5Agg')  # Use Qt5Agg backend for compatibility with PyQt6
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm

# Set Times New Roman font with fallback for professional look
try:
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    if 'Times New Roman' in available_fonts:
        plt.rcParams['font.family'] = 'Times New Roman'
    else:
        plt.rcParams['font.family'] = 'serif'
except:
    plt.rcParams['font.family'] = 'serif'

plt.rcParams['font.size'] = 12

def animate(schedule, processes, colors, interval=800):
    """
    Professional animated Gantt chart for FCFS scheduling
    Compatible version without problematic alpha parameters
    """
    if not schedule:
        print("No schedule to animate!")
        return None
    
    # Create figure with enhanced dark theme and optimal spacing
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    # Adjust layout for better organization with more space for metrics
    plt.subplots_adjust(top=0.88, bottom=0.12, left=0.08, right=0.95)
    
    # Add Idle color if not present
    if "Idle" in schedule and "Idle" not in colors:
        colors["Idle"] = "#404040"

    # Compute completion times for metrics calculation
    completion_times = {}
    for name, _, _ in processes:
        completion_times[name] = 0

    def update(frame):
        ax.clear()
        ax.set_facecolor('#1a1a1a')
        
        # Set up the plot with enhanced professional styling and better spacing
        ax.set_xlim(-0.8, len(schedule) + 0.8)
        ax.set_ylim(-1.8, 3.5)
        ax.set_xlabel("Time Units", fontsize=14, fontweight='bold', color='#FFD700')
        ax.set_ylabel("")
        ax.set_yticks([])
        
        # Professional axis styling
        for spine in ax.spines.values():
            spine.set_color('#FFD700')
            spine.set_linewidth(2)
        ax.tick_params(colors='white', labelsize=12)
        
        # Add professional grid system (simplified)
        for i in range(len(schedule) + 1):
            ax.axvline(x=i, color='#FFD700', linestyle='-', linewidth=1.5)
        
        # Add horizontal reference lines
        ax.axhline(y=0.2, color='#FFD700', linestyle='-', linewidth=1)
        ax.axhline(y=0.8, color='#FFD700', linestyle='-', linewidth=1)
        
        # Add basic grid
        ax.grid(True, color='#444444', linestyle=':', linewidth=0.5)
        
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
        
        # Draw all segments with simplified styling
        for proc, segs in segments.items():
            color = colors.get(proc, '#666666')
            
            # Create properly spaced and aligned bars
            bar_height = 0.6
            bar_y_pos = 0.2
            
            bars = ax.broken_barh(segs, (bar_y_pos, bar_height), 
                                facecolors=color, 
                                edgecolors='#FFD700', 
                                linewidth=2.5)
            
            # Add text labels in segments
            for start, width in segs:
                if width >= 0.8:
                    ax.text(start + width/2, 0.5, proc,
                           ha='center', va='center', color='white', 
                           fontsize=12, fontweight='bold')
        
        # Professional time axis
        time_ticks = list(range(len(schedule) + 1))
        ax.set_xticks(time_ticks)
        ax.set_xticklabels([str(i) for i in time_ticks], 
                          color='white', fontsize=12, fontweight='bold')
        
        # Professional title
        main_title = "FCFS CPU Scheduling Algorithm"
        ax.text(len(schedule)/2, -0.4, main_title, 
               fontsize=18, fontweight='bold', color='#FFD700',
               ha='center', va='center')
        
        # Status information
        current_proc = schedule[frame] if frame < len(schedule) else "Complete"
        progress = f"Time Unit {frame + 1}/{len(schedule)}" if frame < len(schedule) else "Animation Complete"
        status_text = f"Currently Running: {current_proc} | {progress}"
        ax.text(len(schedule)/2, -0.75, status_text,
               fontsize=12, fontweight='bold', color='white',
               ha='center', va='center')
        
        # Create organized metrics display with proper spacing
        metrics_y_start = 2.8
        
        # Title for metrics section
        ax.text(len(schedule)/2, metrics_y_start, "Real-time Process Metrics", 
               fontsize=16, fontweight='bold', color='#FFD700',
               ha='center', va='center')
        
        # Calculate metrics
        total_tat = 0
        total_wt = 0
        active_processes = 0
        
        # Organize processes in a clean grid layout
        num_processes = len(processes)
        if num_processes <= 2:
            # Single row for 1-2 processes
            cols = num_processes
            rows = 1
        elif num_processes <= 4:
            # 2x2 grid for 3-4 processes
            cols = 2
            rows = 2
        else:
            # 3x2 grid for 5 processes
            cols = 3
            rows = 2
        
        # Calculate spacing within the visible chart bounds
        # Chart X-limits are from -0.8 to len(schedule) + 0.8
        chart_left = -0.6   # Stay within left boundary with buffer
        chart_right = len(schedule) + 0.6  # Stay within right boundary with buffer
        available_width = chart_right - chart_left
        col_spacing = available_width / cols
        row_spacing = 0.5
        
        # Calculate starting X position to properly position the grid
        start_x = chart_left + col_spacing / 2
        
        for i, (name, at, bt) in enumerate(processes):
            ct = completion_times[name]
            tat = ct - at if ct > 0 else 0
            wt = tat - bt if tat >= bt else 0
            
            if ct > 0:
                total_tat += tat
                total_wt += wt
                active_processes += 1
            
            # Status indicators with better colors
            if ct > 0:
                status_color = '#90EE90'  # Light green
                status_text = "✓ Completed"
            elif any(proc == name for proc in schedule[:frame+1]):
                status_color = '#FFD700'  # Gold
                status_text = "⚡ Running"
            else:
                status_color = '#FFA500'  # Orange
                status_text = "⏳ Waiting"
            
            # Calculate clean grid positions with proper bounds
            col = i % cols
            row = i // cols
            
            x_pos = start_x + (col * col_spacing)
            y_pos = metrics_y_start - 0.7 - (row * row_spacing)
            
            # Clean, well-spaced metrics text
            metrics_text = f"{name}: CT={ct} | TAT={tat} | WT={wt}\n{status_text}"
            ax.text(x_pos, y_pos, metrics_text, 
                   fontsize=11, color=status_color, fontweight='bold',
                   ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='#2d2d2d', 
                           edgecolor=status_color, linewidth=1))
        
        # Summary statistics positioned above the process metrics
        if active_processes > 0:
            avg_tat = total_tat / active_processes
            avg_wt = total_wt / active_processes
            
            # Position the summary well above the Gantt chart
            summary_y = metrics_y_start - 0.3  # Move up to avoid chart overlap
            summary_text = f"Avg TAT: {avg_tat:.1f} | Avg WT: {avg_wt:.1f} | Completed: {active_processes}/{len(processes)}"
            ax.text(len(schedule)/2, summary_y, summary_text,
                   fontsize=13, fontweight='bold', color='#87CEEB',
                   ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.4", facecolor='#1e3d59', 
                           edgecolor='#87CEEB', linewidth=2))
    
    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=len(schedule), 
                                 interval=interval, repeat=True, blit=False)
    
    plt.show()
    return ani