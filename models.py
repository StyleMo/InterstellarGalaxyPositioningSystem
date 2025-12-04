class Location:
    """DOMAIN MODEL: Represents a location with name, type, and 3D coordinates."""
    
    def __init__(self, name, location_type, position):
        self.name = name
        self.location_type = location_type
        self.position = position  # (x, y, z) coordinates

    def print_location(self):
        print(f"Name: {self.name}, Type: {self.location_type}, Position: {self.position}")

    def set_name(self, name):
        self.name = name

    def set_type(self, location_type):
        self.location_type = location_type

    def set_position(self, position):
        self.position = position

    def __repr__(self):
        return f"Location({self.name}, {self.location_type}, {self.position})"


class Route:
    """DOMAIN MODEL: Represents a route with multiple locations."""
    
    def __init__(self, locations):
        self.locations = locations
        self.starting_location = locations[0] if locations else None
        self.ending_location = locations[-1] if locations else None
        self.total_distance = 0

    def set_starting_location(self, location):
        """Set the starting location."""
        if self.locations:
            self.locations[0] = location
        else:
            self.locations.append(location)
        self.starting_location = location

    def set_ending_location(self, location):
        """Set the ending location."""
        if self.locations:
            self.locations[-1] = location
        else:
            self.locations.append(location)
        self.ending_location = location

    def add_stop(self, location, index=None):
        """Add a stop to the route at a specific index, or at the end."""
        if index is not None:
            self.locations.insert(index, location)
        else:
            self.locations.append(location)
        self.ending_location = self.locations[-1]

    def remove_stop(self, index):
        """Remove a stop from the route."""
        if 0 <= index < len(self.locations):
            self.locations.pop(index)
            if self.locations:
                self.starting_location = self.locations[0]
                self.ending_location = self.locations[-1]
            return True
        return False

    def __repr__(self):
        return f"Route with {len(self.locations)} locations"


class Member:
    """DOMAIN MODEL: Represents a registered member of the IGPS system."""
    
    def __init__(self, member_id, name, home=None, work=None):
        self.member_id = member_id
        self.name = name
        self.home = home
        self.work = work
        self.saved_locations = []
        self.saved_routes = []

    def save_location(self, location):
        """Save a location for quick access."""
        self.saved_locations.append(location)
        print(f"Location saved for member {self.name}.")

    def save_route(self, route):
        """Save a route for future use."""
        self.saved_routes.append(route)
        print(f"Route saved for member {self.name}.")

    def set_home(self, location):
        """Set home location."""
        self.home = location
        print(f"Home location set for {self.name}.")

    def set_work(self, location):
        """Set work location."""
        self.work = location
        print(f"Work location set for {self.name}.")

    def __repr__(self):
        return f"Member({self.member_id}, {self.name})"
