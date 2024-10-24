from dataclasses import dataclass
from typing import Tuple, Dict
from datetime import datetime
import json
from functools import lru_cache
from geopy.distance import geodesic
'''
@dataclass is a decorator that automatically adds things like __init__ and __repr__ methods to the class

This class defines a geofence zone with:
name: identifier for the zone (e.g., "home", "campus")
coordinates: latitude and longitude as a tuple
radius: size of the zone in meters
dwell_time: how long someone needs to stay in the zone before being considered "in" it (in seconds)
'''

@dataclass
class GeofenceZone:
    name: str
    coordinates: Tuple[float, float]
    radius: float
    dwell_time: int = 0

# The GeofenceStatus class initialization:
class GeofenceStatus:
    def __init__(self):
        self._last_status = {}
        self._manager = GeofenceManager()
        self._setup_default_zones()

''' 
Setting up default zones:
Creates two default zones: home and campus
Each has different radius and dwell time requirements
The coordinates are specific to your locations
'''
    def _setup_default_zones(self):
        self._manager.add_zone(GeofenceZone(
            name="home",
            coordinates=(37.688682, -97.336553),  # home coordinates
            radius=100,  # 100 meters
            dwell_time=60  # 1 minute dwell time
        ))

        self._manager.add_zone(GeofenceZone(
            name="campus",
            coordinates=(37.7165348, -97.2959726),  # campus coordinates
            radius=200,  # 200 meters
            dwell_time=180  # 3 minutes dwell time
        ))

''' Status updating:
Takes new coordinates and a device ID
Gets the current status from the manager
Saves it in _last_status dictionary
Returns the status
'''
    def update_status(self, coordinates: Tuple[float, float], device_id: str = "default") -> Dict:
        """Update and return the status for a device."""
        status = self._manager.get_device_status(device_id, coordinates)
        self._last_status[device_id] = status
        return status

'''Status checking methods:
get_current_status: Returns a human-readable status ("is Home", "at Campus", "is Away")
get_status_color: Returns the color code for the GUI (#246CF9 for blue, #FA2256 for red)
Both methods check if we have data for the device first
'''
    def get_current_status(self, device_id: str = "default") -> str:
        """Get the current status string for the GUI."""
        if device_id not in self._last_status:
            return "Unknown"

        status = self._last_status[device_id]
        if status['zones']['home']['in_zone']:
            return "is Home"
        elif status['zones']['campus']['in_zone']:
            return "at Campus"
        return "is Away"

    def get_status_color(self, device_id: str = "default") -> str:
        """Get the status color for the GUI."""
        if device_id not in self._last_status:
            return "#FA2256"  # Red for unknown

        status = self._last_status[device_id]
        if status['zones']['home']['in_zone'] or status['zones']['campus']['in_zone']:
            return "#246CF9"  # Blue for in zone
        return "#FA2256"  # Red for away

'''Here's an example of how it works in practice:
# Create the geofence status manager
status_manager = GeofenceStatus()

# Update with new coordinates
new_location = (37.688685, -97.336550)  # Near home
status = status_manager.update_status(new_location, "my_device")

# Get status for display
current_status = status_manager.get_current_status("my_device")  # "is Home"
status_color = status_manager.get_status_color("my_device")     # "#246CF9" (blue)

# If person moves away
new_location = (37.700000, -97.400000)  # Far from both zones
status = status_manager.update_status(new_location, "my_device")
current_status = status_manager.get_current_status("my_device")  # "is Away"
status_color = status_manager.get_status_color("my_device")     # "#FA2256" (red)

The key features are:
1. Multiple zones with different sizes
2. Dwell time requirements (must stay in zone for X seconds)
3. Support for multiple devices
4. Simple status checking for the GUI
5. Color coding for visual feedback
'''