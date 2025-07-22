from models import Mission, Waypoint
from data_ingestion import get_simulated_flights
from deconfliction import check_mission_conflicts
from visualization import plot_mission_and_conflicts

def main():
    # Define a sample primary mission (conflict and conflict-free example)
    mission = Mission(
        waypoints=[
            Waypoint(x=0, y=5, z=10, t=0),
            Waypoint(x=10, y=5, z=10, t=10),
            Waypoint(x=20, y=5, z=10, t=20),
        ],
        t_start=0,
        t_end=20
    )
    simulated_flights = get_simulated_flights()
    result = check_mission_conflicts(mission, simulated_flights)
    print("Mission Deconfliction Result:")
    print(result['status'])
    print(result['explanation'])
    if result['conflicts']:
        for c in result['conflicts']:
            print(f"Time: {c['time']}, Location: {c['location']}, Other Drone: {c['other_drone']}, Distance: {c['distance']:.2f}m")
    # 3D Visualization
    plot_mission_and_conflicts(mission, simulated_flights, result['conflicts'])

if __name__ == "__main__":
    main() 