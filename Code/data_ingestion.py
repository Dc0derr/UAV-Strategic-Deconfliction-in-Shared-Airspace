import json
from typing import List
from models import FlightPath, Waypoint

def get_simulated_flights(from_file: bool = False, file_path: str = None) -> List[FlightPath]:
    """
    Returns a list of simulated FlightPath objects. Can load from file or use hardcoded data.
    """
    if from_file and file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)
        flights = []
        for entry in data:
            waypoints = [Waypoint(**wp) for wp in entry['waypoints']]
            flights.append(FlightPath(drone_id=entry['drone_id'], waypoints=waypoints))
        return flights
    else:
        # Hardcoded example data with a conflict
        flights = [
            FlightPath(
                drone_id="drone_1",
                waypoints=[
                    Waypoint(x=0, y=0, z=10, t=0),
                    Waypoint(x=10, y=0, z=10, t=10),
                    Waypoint(x=20, y=0, z=10, t=20),
                ]
            ),
            FlightPath(
                drone_id="drone_2",
                waypoints=[
                    Waypoint(x=0, y=10, z=10, t=0),
                    Waypoint(x=10, y=10, z=10, t=10),
                    Waypoint(x=20, y=10, z=10, t=20),
                ]
            ),
            # Conflict drone: crosses y=5 at the same time as the primary mission
            FlightPath(
                drone_id="conflict_drone",
                waypoints=[
                    Waypoint(x=0, y=0, z=10, t=0),
                    Waypoint(x=10, y=10, z=10, t=10),
                    Waypoint(x=20, y=0, z=10, t=20),
                ]
            ),
        ]
        return flights 