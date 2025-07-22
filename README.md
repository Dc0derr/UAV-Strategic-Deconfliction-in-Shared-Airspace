# UAV Strategic Deconfliction System

## Overview
This project implements a strategic deconfliction system for drones in shared airspace. It checks if a primary drone's waypoint mission is safe to execute, considering the simulated flight paths of other drones in both space and time.

## Features
- Spatial and temporal conflict detection
- Detailed conflict explanations
- 3D and animated visualization of missions and conflicts
- Modular, extensible codebase

## Requirements
- Python 3.8+
- matplotlib

## Setup
1. Clone the repository or download the code.
2. Install dependencies:
   ```bash
   pip install matplotlib
   ```

## Usage
Run the main script to check a sample mission and print results:
```bash
python main.py
```

To visualize missions and conflicts, use the functions in `visualization.py`:
- `plot_mission_and_conflicts(mission, simulated_flights, conflicts)`
- `animate_mission(mission, simulated_flights, conflicts)`

## File Structure
- `models.py`: Data classes for waypoints, flight paths, and missions
- `data_ingestion.py`: Load simulated drone schedules
- `deconfliction.py`: Core logic for conflict detection
- `visualization.py`: Plotting and animation
- `main.py`: Example usage and interface
- `tests/`: (To be added) Automated tests

## Extending
- Add more drones or missions by editing `data_ingestion.py` or providing a JSON file
- Adjust safety buffer and time step in `deconfliction.py`

## License
MIT 