import numpy as np


class LocationsDatabase:
    """Data Access Layer: Manages all locations in the galaxy."""

    def __init__(self):
        self.location_types = set()
        self.all_locations = {}  # Dictionary for O(1) lookup by name

    def add_location(self, location):
        """Add a location to the database."""
        if location.name in self.all_locations:
            print(f"Location '{location.name}' already exists.")
            return False

        # Validate coordinates are within galaxy bounds
        if not self._check_coordinates(location.position):
            print(f"Note: Location '{location.name}' has coordinates outside typical galaxy bounds.")

        self.all_locations[location.name] = location
        self.location_types.add(location.location_type)
        print(f"Location '{location.name}' added successfully.")
        return True

    def _check_coordinates(self, position):
        """Internal method to check if coordinates are reasonable."""
        # Radius: 50,000 Light Years
        # Height: ±500 Light Years
        x, y, z = position
        radius = np.sqrt(x**2 + z**2)
        return radius <= 50000 and abs(y) <= 500

    def remove_location(self, location_name):
        """Remove a location from the database."""
        if location_name not in self.all_locations:
            print(f"Location '{location_name}' not found.")
            return False
        del self.all_locations[location_name]
        print(f"Location '{location_name}' removed successfully.")
        return True

    def edit_location(self, location_name, new_name=None, new_type=None, new_position=None):
        """Edit an existing location's details."""
        if location_name not in self.all_locations:
            print(f"Location '{location_name}' not found.")
            return False

        location = self.all_locations[location_name]

        if new_name and new_name != location_name:
            if new_name in self.all_locations:
                print(f"Location name '{new_name}' already exists.")
                return False
            del self.all_locations[location_name]
            location.set_name(new_name)
            self.all_locations[new_name] = location

        if new_type:
            location.set_type(new_type)
            self.location_types.add(new_type)

        if new_position:
            location.set_position(new_position)

        print(f"Location updated successfully.")
        return True

    def location_information(self, location_name):
        """Get information about a specific location."""
        return self.all_locations.get(location_name)

    def location_exists(self, location_name):
        """Check if a location exists in the database."""
        return location_name in self.all_locations
