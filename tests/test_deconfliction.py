import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from models import Mission, Waypoint, FlightPath
from deconfliction import check_mission_conflicts

def test_conflict_free():
    mission = Mission(
        waypoints=[Waypoint(x=0, y=0, z=10, t=0), Waypoint(x=10, y=0, z=10, t=10)],
        t_start=0, t_end=10
    )
    flights = [
        FlightPath(drone_id="sim1", waypoints=[Waypoint(x=0, y=20, z=10, t=0), Waypoint(x=10, y=20, z=10, t=10)])
    ]
    result = check_mission_conflicts(mission, flights)
    assert result['status'] == 'clear'
    assert not result['conflicts']

def test_conflict_present():
    mission = Mission(
        waypoints=[Waypoint(x=0, y=0, z=10, t=0), Waypoint(x=10, y=0, z=10, t=10)],
        t_start=0, t_end=10
    )
    flights = [
        FlightPath(drone_id="sim1", waypoints=[Waypoint(x=0, y=0, z=10, t=0), Waypoint(x=10, y=0, z=10, t=10)])
    ]
    result = check_mission_conflicts(mission, flights)
    assert result['status'] == 'conflict detected'
    assert result['conflicts']

def test_edge_case_near_miss():
    mission = Mission(
        waypoints=[Waypoint(x=0, y=0, z=10, t=0), Waypoint(x=10, y=0, z=10, t=10)],
        t_start=0, t_end=10
    )
    flights = [
        FlightPath(drone_id="sim1", waypoints=[Waypoint(x=0, y=5.1, z=10, t=0), Waypoint(x=10, y=5.1, z=10, t=10)])
    ]
    result = check_mission_conflicts(mission, flights, safety_buffer=5.0)
    assert result['status'] == 'clear'
    assert not result['conflicts']

def test_3d_conflict():
    mission = Mission(
        waypoints=[Waypoint(x=0, y=0, z=10, t=0), Waypoint(x=10, y=0, z=10, t=10)],
        t_start=0, t_end=10
    )
    flights = [
        FlightPath(drone_id="sim1", waypoints=[Waypoint(x=0, y=0, z=12, t=0), Waypoint(x=10, y=0, z=12, t=10)])
    ]
    result = check_mission_conflicts(mission, flights, safety_buffer=3.0)
    assert result['status'] == 'conflict detected'
    assert result['conflicts'] 