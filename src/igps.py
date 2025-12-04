import numpy as np
from src.models import Location, Route


class IGPS:
    """BUSINESS LOGIC LAYER: Intelligent Galaxy Positioning System"""

    # Milky Way Galaxy specifications
    GALAXY_RADIUS = 50000  # Light Years
    GALAXY_HEIGHT = 500    # Light Years (half-height from center)

    # Average spacecraft specifications
    AVG_SPEED_MIN = 50
    AVG_SPEED_MAX = 100
    AVG_SPEED = 75
    FUEL_EFFICIENCY = 250  # Light Years per gallon
    TANK_CAPACITY = 15     # gallons
    MAX_RANGE = FUEL_EFFICIENCY * TANK_CAPACITY

    # Conversion constants
    LIGHT_MINUTES_PER_LIGHT_YEAR = 525600  # 60 min/hr * 24 hr/day * 365.25 days/year

    def __init__(self, database):
        self.database = database

    @staticmethod
    def light_years_to_light_minutes(light_years):
        """Convert light years to light minutes."""
        return light_years * IGPS.LIGHT_MINUTES_PER_LIGHT_YEAR

    @staticmethod
    def light_minutes_to_light_years(light_minutes):
        """Convert light minutes to light years."""
        return light_minutes / IGPS.LIGHT_MINUTES_PER_LIGHT_YEAR

    @staticmethod
    def format_distance(light_years):
        """Format distance in the most readable unit (light minutes or light years)."""
        if light_years < 0.01:
            light_minutes = IGPS.light_years_to_light_minutes(light_years)
            return f"{light_minutes:.2f} light minutes"
        else:
            return f"{light_years:.2f} light years"

    @staticmethod
    def calculate_distance_between(loc1, loc2):
        """Calculate Euclidean distance between two locations in 3D space using NumPy."""
        pos1 = np.array(loc1.position if isinstance(loc1, Location) else loc1)
        pos2 = np.array(loc2.position if isinstance(loc2, Location) else loc2)
        return np.linalg.norm(pos2 - pos1)

    def get_location(self, location_input):
        """Get a location from database by name, or return coordinates directly."""
        if isinstance(location_input, str):
            location = self.database.location_information(location_input)
            if location is None:
                print(f"Error: Location '{location_input}' does not exist in the database.")
                return None
            return location
        elif isinstance(location_input, tuple) and len(location_input) == 3:
            return location_input
        else:
            print("Invalid location input. Must be a location name or (x, y, z) coordinates.")
            return None

    def location_information(self, location_input):
        """Display information about a location."""
        location = self.get_location(location_input)
        if location:
            if isinstance(location, Location):
                location.print_location()
            else:
                print(f"Coordinates: {location}")

    def calculate_route_distance(self, route):
        """Calculate total distance for a route."""
        total_distance = 0
        for i in range(len(route.locations) - 1):
            total_distance += self.calculate_distance_between(route.locations[i], route.locations[i + 1])
        route.total_distance = total_distance
        return total_distance

    def display_route_segments(self, route):
        """Display each segment of the route with distances."""
        print("Route segments:")
        for i in range(len(route.locations) - 1):
            loc1 = route.locations[i]
            loc2 = route.locations[i + 1]
            distance = self.calculate_distance_between(loc1, loc2)

            name1 = loc1.name if isinstance(loc1, Location) else f"Coordinates {loc1}"
            name2 = loc2.name if isinstance(loc2, Location) else f"Coordinates {loc2}"

            print(f"  {name1} -> {name2}: {self.format_distance(distance)}")

    def create_route(self, location_inputs):
        """Create a route from a list of location names or coordinates."""
        if len(location_inputs) < 2:
            print("Error: A route must have at least 2 locations.")
            return None

        locations = []
        for loc_input in location_inputs:
            loc = self.get_location(loc_input)
            if loc is None:
                return None
            locations.append(loc)

        route = Route(locations)
        distance = self.calculate_route_distance(route)
        print(f"Route created with total distance: {self.format_distance(distance)}")
        return route

    def optimize_route(self, location_inputs):
        """Create an optimized route using nearest neighbor algorithm (approximation for TSP)."""
        if len(location_inputs) < 2:
            print("Error: A route must have at least 2 locations.")
            return None

        locations = []
        for loc_input in location_inputs:
            loc = self.get_location(loc_input)
            if loc is None:
                return None
            locations.append(loc)

        if len(locations) == 2:
            return Route(locations)

        # Start with first location, then use nearest neighbor
        optimized = [locations[0]]
        remaining = locations[1:]

        while remaining:
            current = optimized[-1]
            nearest = min(remaining, key=lambda loc: self.calculate_distance_between(current, loc))
            optimized.append(nearest)
            remaining.remove(nearest)

        route = Route(optimized)
        distance = self.calculate_route_distance(route)
        print(f"Optimized route created with total distance: {self.format_distance(distance)}")
        return route

    def calculate_fuel_required(self, route):
        """Calculate fuel required for a route in gallons."""
        if route.total_distance == 0:
            self.calculate_route_distance(route)

        fuel_gallons = route.total_distance / self.FUEL_EFFICIENCY
        print(f"Route distance: {self.format_distance(route.total_distance)}")
        print(f"Fuel required: {fuel_gallons:.2f} gallons")

        if fuel_gallons > self.TANK_CAPACITY:
            refuel_stops = int(fuel_gallons / self.TANK_CAPACITY)
            print(f"WARNING: Route exceeds single tank capacity!")
            print(f"You will need approximately {refuel_stops} refueling stop(s)")

        return fuel_gallons

    def calculate_travel_time(self, route, speed=None):
        """Calculate estimated travel time for a route in hours."""
        if speed is None:
            speed = self.AVG_SPEED

        if route.total_distance == 0:
            self.calculate_route_distance(route)

        time_hours = route.total_distance / speed

        days = int(time_hours / 24)
        hours = int(time_hours % 24)
        minutes = int((time_hours % 1) * 60)

        print(f"Estimated travel time at {speed} LY/hr:")
        if days > 0:
            print(f"  {days} days, {hours} hours, {minutes} minutes")
        elif hours > 0:
            print(f"  {hours} hours, {minutes} minutes")
        else:
            print(f"  {minutes} minutes")

        return time_hours

    def validate_coordinates(self, position):
        """Check if coordinates are within the Milky Way galaxy bounds."""
        x, y, z = position

        radius_from_center = np.sqrt(x**2 + z**2)
        if radius_from_center > self.GALAXY_RADIUS:
            print(f"WARNING: Coordinates ({x}, {y}, {z}) are outside galaxy radius!")
            print(f"Distance from center: {radius_from_center:.2f} LY (max: {self.GALAXY_RADIUS} LY)")
            return False

        if abs(y) > self.GALAXY_HEIGHT:
            print(f"WARNING: Y-coordinate {y} exceeds galaxy height!")
            print(f"Galaxy height range: -{self.GALAXY_HEIGHT} to +{self.GALAXY_HEIGHT} LY")
            return False

        return True

    def add_stop_to_route(self, route, location_input):
        """Add a stop to an existing route and automatically optimize its position for minimum distance.
        The new stop will never become the starting location - it can only be inserted between
        existing stops or at the end."""
        location = self.get_location(location_input)
        if location is None:
            return False

        if len(route.locations) < 2:
            route.add_stop(location)
            self.calculate_route_distance(route)
            print(f"Stop added. New total distance: {self.format_distance(route.total_distance)}")
            return True

        # Try inserting the new location at each possible position EXCEPT position 0 (start)
        best_index = len(route.locations)  # Default: add at end
        best_distance = float('inf')

        for i in range(1, len(route.locations) + 1):  # Start from 1, not 0
            temp_locations = route.locations.copy()
            temp_locations.insert(i, location)
            temp_route = Route(temp_locations)
            temp_distance = self.calculate_route_distance(temp_route)

            if temp_distance < best_distance:
                best_distance = temp_distance
                best_index = i

        route.locations.insert(best_index, location)
        route.starting_location = route.locations[0]
        route.ending_location = route.locations[-1]
        self.calculate_route_distance(route)

        loc_name = location.name if isinstance(location, Location) else f"Coordinates {location}"
        print(f"Stop '{loc_name}' added at optimal position {best_index}.")
        print(f"New total distance: {self.format_distance(route.total_distance)}")
        return True
