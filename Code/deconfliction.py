import math
from typing import List, Dict, Any, Tuple
from models import Mission, FlightPath, Waypoint

def interpolate_waypoints(waypoints: List[Waypoint], t_start: float, t_end: float, time_step: float) -> Dict[float, Tuple[float, float, float]]:
    """
    Linearly interpolate waypoints to get position at each time step.
    Returns a dict: {time: (x, y, z)}
    """
    if not waypoints:
        return {}
    positions = {}
    times = [wp.t for wp in waypoints if wp.t is not None]
    if not times:
        return {}
    min_t, max_t = min(times), max(times)
    t = max(t_start, min_t)
    while t <= min(t_end, max_t):
        # Find segment
        for i in range(len(waypoints) - 1):
            wp1, wp2 = waypoints[i], waypoints[i+1]
            if wp1.t is not None and wp2.t is not None and wp1.t <= t <= wp2.t:
                ratio = (t - wp1.t) / (wp2.t - wp1.t) if wp2.t != wp1.t else 0
                x = wp1.x + ratio * (wp2.x - wp1.x)
                y = wp1.y + ratio * (wp2.y - wp1.y)
                z = (wp1.z or 0) + ratio * ((wp2.z or 0) - (wp1.z or 0))
                positions[t] = (x, y, z)
                break
        t += time_step
    return positions

def euclidean_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def check_mission_conflicts(
    mission: Mission,
    simulated_flights: List[FlightPath],
    safety_buffer: float = 5.0,
    time_step: float = 1.0
) -> Dict[str, Any]:
    """
    Checks for spatial and temporal conflicts between the mission and simulated flights.
    Returns a dict with status and conflict details.
    """
    # Interpolate primary mission
    mission_positions = interpolate_waypoints(mission.waypoints, mission.t_start, mission.t_end, time_step)
    conflicts = []
    for sim_flight in simulated_flights:
        sim_positions = interpolate_waypoints(sim_flight.waypoints, mission.t_start, mission.t_end, time_step)
        for t, m_pos in mission_positions.items():
            if t in sim_positions:
                s_pos = sim_positions[t]
                dist = euclidean_distance(m_pos, s_pos)
                if dist < safety_buffer:
                    conflicts.append({
                        'time': t,
                        'location': {'x': m_pos[0], 'y': m_pos[1], 'z': m_pos[2]},
                        'other_drone': sim_flight.drone_id,
                        'distance': dist
                    })
    if conflicts:
        return {
            'status': 'conflict detected',
            'conflicts': conflicts,
            'explanation': f"{len(conflicts)} conflict(s) found. See details."
        }
    else:
        return {
            'status': 'clear',
            'conflicts': [],
            'explanation': 'No conflicts detected.'
        } 