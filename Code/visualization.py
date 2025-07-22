import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from models import Mission, FlightPath
from typing import List, Dict, Any

def plot_mission_and_conflicts(mission: Mission, simulated_flights: List[FlightPath], conflicts: List[Dict[str, Any]]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot primary mission
    mx = [wp.x for wp in mission.waypoints]
    my = [wp.y for wp in mission.waypoints]
    mz = [wp.z if wp.z is not None else 0 for wp in mission.waypoints]
    ax.plot(mx, my, mz, label='Primary Mission', color='blue', marker='o')
    # Plot simulated flights
    for flight in simulated_flights:
        fx = [wp.x for wp in flight.waypoints]
        fy = [wp.y for wp in flight.waypoints]
        fz = [wp.z if wp.z is not None else 0 for wp in flight.waypoints]
        ax.plot(fx, fy, fz, label=f"Sim {flight.drone_id}", linestyle='--', marker='x')
    # Plot conflicts
    if conflicts:
        cx = [c['location']['x'] for c in conflicts]
        cy = [c['location']['y'] for c in conflicts]
        cz = [c['location']['z'] for c in conflicts]
        ax.scatter(cx, cy, cz, color='red', s=60, label='Conflicts')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Altitude)')
    ax.legend()
    plt.title('Mission and Simulated Flights with Conflicts')
    plt.show()

def animate_mission(mission: Mission, simulated_flights: List[FlightPath], conflicts: List[Dict[str, Any]] = None):
    # Optional: Animate the mission and flights over time (2D for simplicity)
    import matplotlib.animation as animation
    fig, ax = plt.subplots()
    # Prepare data
    mx = [wp.x for wp in mission.waypoints]
    my = [wp.y for wp in mission.waypoints]
    # Plot static simulated flights
    for flight in simulated_flights:
        fx = [wp.x for wp in flight.waypoints]
        fy = [wp.y for wp in flight.waypoints]
        ax.plot(fx, fy, linestyle='--', marker='x', label=f"Sim {flight.drone_id}")
    # Animate primary mission
    line, = ax.plot([], [], 'bo-', label='Primary Mission')
    conflict_scatter = ax.scatter([], [], color='red', s=60, label='Conflicts')
    ax.set_xlim(min(mx)-5, max(mx)+5)
    ax.set_ylim(min(my)-5, max(my)+5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    def update(frame):
        line.set_data(mx[:frame+1], my[:frame+1])
        if conflicts:
            cx = [c['location']['x'] for c in conflicts if c['time'] <= mission.waypoints[frame].t]
            cy = [c['location']['y'] for c in conflicts if c['time'] <= mission.waypoints[frame].t]
            conflict_scatter.set_offsets(list(zip(cx, cy)))
        return line, conflict_scatter
    ani = animation.FuncAnimation(fig, update, frames=len(mx), interval=1000, blit=False, repeat=False)
    plt.title('Mission Animation')
    plt.show() 