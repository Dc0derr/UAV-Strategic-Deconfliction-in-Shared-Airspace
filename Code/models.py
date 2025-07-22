from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Waypoint:
    x: float
    y: float
    z: Optional[float] = None  # Altitude (optional, for 3D)
    t: Optional[float] = None  # Timestamp (seconds or any consistent unit)

@dataclass
class FlightPath:
    drone_id: str
    waypoints: List[Waypoint]
    # Optionally, add more metadata if needed

@dataclass
class Mission:
    waypoints: List[Waypoint]
    t_start: float
    t_end: float
    # Optionally, add mission id or metadata 