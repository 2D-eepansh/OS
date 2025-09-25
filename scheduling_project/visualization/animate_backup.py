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

# Configure matplotlib for better animation performance
plt.rcParams['animation.html'] = 'html5'

def animate(schedule, processes, colors, interval=800):
    """
    Professional animated Gantt chart for FCFS scheduling
    Integrated with modern PyQt6 GUI theme
    """
    if not schedule:
        print("No schedule to animate!")
        return None
    
    # Create figure with enhanced dark theme and better spacing
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    # Adjust layout for better organization
    plt.subplots_adjust(top=0.85, bottom=0.15, left=0.08, right=0.95)
    
    # Add Idle color if not present
    if "Idle" in schedule and "Idle" not in colors:
        colors["Idle"] = "#404040"

    # Compute completion times for metrics calculation
    completion_times = {}
    for name, at, bt in processes:
        completion_times[name] = 0
    
    def update(frame):
        ax.clear()
        ax.set_facecolor('#1a1a1a')
        
        # Set up the plot with proper alignment - start at 0
        ax.set_xlim(-0.8, len(schedule) + 0.8)  # Add buffer space for clean look
        ax.set_ylim(-1.5, 4)
        ax.set_xlabel("Time Units", fontsize=14, fontweight='bold', color='#FFD700')
        ax.set_ylabel("")
        ax.set_yticks([])
        
        # Professional axis styling
        for spine in ax.spines.values():
            spine.set_color('#FFD700')
            spine.set_linewidth(2)
        ax.tick_params(colors='white', labelsize=12)
        
        # Add professional grid system
        # Major grid lines at time boundaries
        for i in range(len(schedule) + 1):
            ax.axvline(x=i, color='#FFD700', linestyle='-', alpha=0.6, linewidth=1.5)
        
        # Add horizontal reference line for the process bar
        ax.axhline(y=0.2, color='#FFD700', linestyle='-', alpha=0.3, linewidth=1)
        ax.axhline(y=0.8, color='#FFD700', linestyle='-', alpha=0.3, linewidth=1)
        
        # Add subtle background grid (without alpha parameter for compatibility)
        ax.grid(True, which='major', color='#444444', linestyle=':', linewidth=0.5)
        
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
        
        # Draw all segments with proper alignment and spacing
        for proc, segs in segments.items():
            color = colors.get(proc, '#666666')
            
            # Create properly spaced and aligned bars
            bar_height = 0.6  # Slightly smaller for cleaner look
            bar_y_pos = 0.2   # Center the bar vertically
            
            bars = ax.broken_barh(segs, (bar_y_pos, bar_height), 
                                facecolors=color, 
                                edgecolors='#FFD700', 
                                linewidth=2.5,
                                alpha=0.9)
            
            # Add text labels in segments with better positioning
            for start, width in segs:
                if width >= 0.8:  # Only show text if segment is wide enough
                    ax.text(start + width/2, 0.5, proc,
                           ha='center', va='center', color='white', 
                           fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.15", 
                                   facecolor='black', alpha=0.4,
                                   edgecolor='white', linewidth=1))
        
        # Professional time axis with proper alignment
        time_ticks = list(range(len(schedule) + 1))
        ax.set_xticks(time_ticks)
        ax.set_xticklabels([str(i) for i in time_ticks], 
                          color='white', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time Units', color='#FFD700', fontsize=14, fontweight='bold', labelpad=10)
        
        # Add minor ticks for better alignment visualization
        minor_ticks = [i + 0.5 for i in range(len(schedule))]
        ax.set_xticks(minor_ticks, minor=True)
        ax.tick_params(which='minor', length=4, color='#FFD700', alpha=0.6)
        
        # Create professional metrics display with better alignment
        y_start = 1.5
        
        # Title section with better positioning
        title_box_props = dict(boxstyle="round,pad=0.4", facecolor='#2d2d2d', 
                              edgecolor='#FFD700', linewidth=2, alpha=0.9)
        ax.text(len(schedule)/2, y_start + 0.8, "Real-time Process Metrics", 
               fontsize=16, fontweight='bold', color='#FFD700',
               ha='center', va='center', bbox=title_box_props)
        
        # Calculate metrics
        total_tat = 0
        total_wt = 0
        active_processes = 0
        
        # Process metrics in organized columns
        col_width = max(8, len(schedule) // 3)
        y_pos = y_start + 0.3
        
        for i, (name, at, bt) in enumerate(processes):
            ct = completion_times[name]
            tat = ct - at if ct > 0 else 0
            wt = tat - bt if tat >= bt else 0
            
            if ct > 0:
                total_tat += tat
                total_wt += wt
                active_processes += 1
            
            # Enhanced status indicators
            if ct > 0:
                status_color = '#90EE90'
                status_icon = "✓"
                status_text = "Completed"
            elif any(proc == name for proc in schedule[:frame+1]):
                status_color = '#FFD700'
                status_icon = "⚡"
                status_text = "Running"
            else:
                status_color = '#FFA500'
                status_icon = "⏳"
                status_text = "Waiting"
            
            # Better formatted process information
            x_pos = i * col_width if i < 3 else (i - 3) * col_width
            y_offset = 0 if i < 3 else -0.35
            
            process_box_props = dict(boxstyle="round,pad=0.25", 
                                   facecolor='#333333', 
                                   edgecolor=status_color, 
                                   linewidth=1.5, alpha=0.8)
            
            metrics_text = f"{name}: CT={ct} | TAT={tat} | WT={wt}\n{status_icon} {status_text}"
            ax.text(x_pos, y_pos + y_offset, metrics_text, 
                   fontsize=10, color=status_color, fontweight='bold',
                   ha='left', va='center', bbox=process_box_props)
        
        # Summary statistics with professional styling
        if active_processes > 0:
            avg_tat = total_tat / active_processes
            avg_wt = total_wt / active_processes
            
            summary_box_props = dict(boxstyle="round,pad=0.4", 
                                   facecolor='#1e3d59', 
                                   edgecolor='#87CEEB', 
                                   linewidth=2, alpha=0.9)
            
            summary_text = f"Avg TAT: {avg_tat:.1f} | Avg WT: {avg_wt:.1f} | Completed: {active_processes}/{len(processes)}"
            ax.text(len(schedule)/2, y_start - 0.4, summary_text,
                   fontsize=12, fontweight='bold', color='#87CEEB',
                   ha='center', va='center', bbox=summary_box_props)
        
        # Professional title with status information
        current_proc = schedule[frame] if frame < len(schedule) else "Complete"
        progress = f"Time Unit {frame + 1}/{len(schedule)}" if frame < len(schedule) else "Animation Complete"
        
        # Main title
        main_title = "FCFS CPU Scheduling Algorithm"
        ax.text(len(schedule)/2, -0.4, main_title, 
               fontsize=18, fontweight='bold', color='#FFD700',
               ha='center', va='center',
               bbox=dict(boxstyle="round,pad=0.5", 
                        facecolor='#1a1a1a', 
                        edgecolor='#FFD700', 
                        linewidth=2, alpha=0.95))
        
        # Status information
        status_text = f"Currently Running: {current_proc} | {progress}"
        ax.text(len(schedule)/2, -0.75, status_text,
               fontsize=12, fontweight='bold', color='white',
               ha='center', va='center',
               bbox=dict(boxstyle="round,pad=0.3", 
                        facecolor='#2d2d2d', alpha=0.8))
        
        # Style the axes
        ax.spines['bottom'].set_color('#FFD700')
        ax.spines['top'].set_color('#FFD700') 
        ax.spines['right'].set_color('#FFD700')
        ax.spines['left'].set_color('#FFD700')
        ax.tick_params(colors='white')
        
        return []

    # Set window title before creating animation
    try:
        fig.canvas.manager.set_window_title("FCFS Scheduling Animation - Professional Edition")
    except:
        pass
    
    # Create animation with smooth timing
    ani = animation.FuncAnimation(
        fig, update, frames=len(schedule),
        interval=interval, repeat=False, blit=False,
        cache_frame_data=False
    )
    
    # Show the plot without blocking
    plt.tight_layout()
    plt.show(block=False)
    
    # Force the first frame to display
    update(0)
    plt.draw()
    
    print("Animation started!")
    return ani


