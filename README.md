# InterstellarGalaxyPositioningSystem
import numpy as np

class Location:
    # DOMAIN MODEL: Represents a location with name, type, and 3D coordinates.
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


class LocationsDatabase:
    # Data Access Layer: Manages all locations in the galaxy.

    def __init__(self):
        self.location_types = set()
        self.all_locations = {}  # Dictionary for O(1) lookup by name

    def add_location(self, location):
        # Add a location to the database.
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
        # Internal method to check if coordinates are reasonable.
        # Radius: 50,000 Light Years
        # Height: ±500 Light Years
        x, y, z = position
        radius = np.sqrt(x**2 + z**2)
        return radius <= 50000 and abs(y) <= 500

    def remove_location(self, location_name):
        # Remove a location from the database.
        if location_name not in self.all_locations:
            print(f"Location '{location_name}' not found.")
            return False
        del self.all_locations[location_name]
        print(f"Location '{location_name}' removed successfully.")
        return True

    def edit_location(self, location_name, new_name=None, new_type=None, new_position=None):
        # """Edit an existing location's details.
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
        # Get information about a specific location.
        return self.all_locations.get(location_name)

    def location_exists(self, location_name):
        """Check if a location exists in the database."""
        return location_name in self.all_locations


class Route:
    # Layer -  DOMAIN MODEL: Represents a route with multiple locations.


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
        # Remove a stop from the route.
        # Check if index is valid
        if 0 <= index < len(self.locations):
            self.locations.pop(index)
            if self.locations:
                self.starting_location = self.locations[0]
                self.ending_location = self.locations[-1]
            return True
        return False  # Return False for invalid index

    def __repr__(self):
        return f"Route with {len(self.locations)} locations"


class IGPS:

    # Layer - BUSINESS LOGIC LAYER: Intelligent Galaxy Positioning System


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
        # If distance is less than 0.01 light years (5,256 light minutes), show in light minutes
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

        # NumPy's norm function calculates the Euclidean distance
        return np.linalg.norm(pos2 - pos1)

    def get_location(self, location_input):
        # Get a location from database by name, or return coordinates directly.

        if isinstance(location_input, str):
            location = self.database.location_information(location_input)
            if location is None:
                # Location not found in database
                print(f"Error: Location '{location_input}' does not exist in the database.")
                return None
            return location
        elif isinstance(location_input, tuple) and len(location_input) == 3:
            # Accept coordinate tuples with 3 elements
            return location_input
        else:
            # Invalid input type
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

        # Get all locations
        locations = []
        for loc_input in location_inputs:
            loc = self.get_location(loc_input)
            if loc is None:
                return None
            locations.append(loc)

        # If only 2 locations, no optimization needed
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

        # Check if route exceeds tank capacity
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

        # Convert to more readable format
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

        # Check if within disk radius
        radius_from_center = np.sqrt(x**2 + z**2)
        if radius_from_center > self.GALAXY_RADIUS:
            print(f"WARNING: Coordinates ({x}, {y}, {z}) are outside galaxy radius!")
            print(f"Distance from center: {radius_from_center:.2f} LY (max: {self.GALAXY_RADIUS} LY)")
            return False

        # Check if within height bounds
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

        # If route has less than 2 locations, just add it at the end
        if len(route.locations) < 2:
            route.add_stop(location)
            self.calculate_route_distance(route)
            print(f"Stop added. New total distance: {self.format_distance(route.total_distance)}")
            return True

        # Try inserting the new location at each possible position EXCEPT position 0 (start)
        # Can insert at positions 1, 2, 3, ..., end
        best_index = len(route.locations)  # Default: add at end
        best_distance = float('inf')

        for i in range(1, len(route.locations) + 1):  # Start from 1, not 0
            # Create a temporary route with the new location at position i
            temp_locations = route.locations.copy()
            temp_locations.insert(i, location)
            temp_route = Route(temp_locations)
            temp_distance = self.calculate_route_distance(temp_route)

            # Check if this is better than the current best
            if temp_distance < best_distance:
                best_distance = temp_distance
                best_index = i

        # Insert at the optimal position (guaranteed to be >= 1)
        route.locations.insert(best_index, location)
        route.starting_location = route.locations[0]  # Starting location unchanged
        route.ending_location = route.locations[-1]
        self.calculate_route_distance(route)

        loc_name = location.name if isinstance(location, Location) else f"Coordinates {location}"
        print(f"Stop '{loc_name}' added at optimal position {best_index}.")
        print(f"New total distance: {self.format_distance(route.total_distance)}")
        return True


class Member:
    # Layer - DOMAIN MODEL: Represents a registered member of the IGPS system.

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


class SystemManager:
    # LAYER - APPLICATION/PRESENTATION LAYER
    # LAYERED ARCHITECTURE - APPLICATION LAYER
    # SystemManager sits at the top of the architecture
    def __init__(self):
        self.members = {}  # Dictionary for O(1) lookup
        self.database = LocationsDatabase()  # Data Access Layer
        self.igps = IGPS(self.database)      # Business Logic Layer

    def register_member(self, member_id, name, home=None, work=None):
        """Register a new member."""
        if member_id in self.members:
            print(f"Member ID '{member_id}' already exists.")
            return None

        member = Member(member_id, name, home, work)
        self.members[member_id] = member
        print(f"Member '{name}' registered successfully with ID: {member_id}")
        return member

    def remove_member(self, member_id):
        """Remove a member from the system."""
        if member_id not in self.members:
            print(f"Member ID '{member_id}' not found.")
            return False

        member_name = self.members[member_id].name
        del self.members[member_id]
        print(f"Member '{member_name}' removed successfully.")
        return True

    def get_member(self, member_id):
        """Get a member by ID."""
        return self.members.get(member_id)

    # Administrator functions for database management
    def admin_add_location(self, location):
        """Administrator: Add a location to the database."""
        return self.database.add_location(location)

    def admin_edit_location(self, location_name, new_name=None, new_type=None, new_position=None):
        """Administrator: Edit a location in the database."""
        return self.database.edit_location(location_name, new_name, new_type, new_position)

    def admin_delete_location(self, location_name):
        """Administrator: Delete a location from the database."""
        return self.database.remove_location(location_name)


# Example usage and tests
if __name__ == "__main__":
    import unittest

    # UNIT TESTS
    # TESTING REQUIREMENT: Unit Testing with unittest framework
    # Each test class tests a specific component with proper assertions
    # Tests cover normal operation, edge cases, and error handling

    class TestLocation(unittest.TestCase):
        """
        UNIT TESTS: Location class
        Tests basic CRUD operations and data integrity
        """

        def test_location_creation(self):
            """Test that a location is created with correct attributes."""
            loc = Location("Earth", "Planet", (0, 0, 0))
            self.assertEqual(loc.name, "Earth")
            self.assertEqual(loc.location_type, "Planet")
            self.assertEqual(loc.position, (0, 0, 0))

        def test_set_name(self):
            """Test that location name can be updated."""
            loc = Location("Earth", "Planet", (0, 0, 0))
            loc.set_name("Terra")
            self.assertEqual(loc.name, "Terra")

        def test_set_type(self):
            """Test that location type can be updated."""
            loc = Location("Earth", "Planet", (0, 0, 0))
            loc.set_type("Home World")
            self.assertEqual(loc.location_type, "Home World")

        def test_set_position(self):
            """Test that location position can be updated."""
            loc = Location("Earth", "Planet", (0, 0, 0))
            loc.set_position((100, 200, 300))
            self.assertEqual(loc.position, (100, 200, 300))


    class TestLocationsDatabase(unittest.TestCase):
        # UNIT TESTS: LocationsDatabase class (Data Access Layer)
        # Tests error handling, and input validation

        def setUp(self):
            """Set up a fresh database for each test."""
            self.db = LocationsDatabase()
            self.earth = Location("Earth", "Planet", (0, 0, 0))
            self.mars = Location("Mars", "Planet", (10, 5, 2))

        def test_add_location(self):
            """Test adding a location to the database."""
            result = self.db.add_location(self.earth)
            self.assertTrue(result)
            self.assertIn("Earth", self.db.all_locations)
            self.assertEqual(self.db.all_locations["Earth"], self.earth)

        def test_add_duplicate_location(self):
            """
            ERROR HANDLING TEST: Adding duplicate location should fail
            Verifies the system prevents data corruption
            """
            self.db.add_location(self.earth)
            result = self.db.add_location(self.earth)
            self.assertFalse(result)

        def test_remove_location(self):
            """Test removing a location from the database."""
            self.db.add_location(self.earth)
            result = self.db.remove_location("Earth")
            self.assertTrue(result)
            self.assertNotIn("Earth", self.db.all_locations)

        def test_remove_nonexistent_location(self):
            """Test that removing a non-existent location fails."""
            result = self.db.remove_location("Jupiter")
            self.assertFalse(result)

        def test_location_exists(self):
            """Test checking if a location exists."""
            self.db.add_location(self.earth)
            self.assertTrue(self.db.location_exists("Earth"))
            self.assertFalse(self.db.location_exists("Mars"))

        def test_location_information(self):
            """Test retrieving location information."""
            self.db.add_location(self.earth)
            loc = self.db.location_information("Earth")
            self.assertEqual(loc, self.earth)

            # Non-existent location should return None
            loc = self.db.location_information("Jupiter")
            self.assertIsNone(loc)

        def test_edit_location(self):
            """Test editing a location's properties."""
            self.db.add_location(self.earth)
            result = self.db.edit_location("Earth", new_name="Terra", new_type="Home")
            self.assertTrue(result)
            self.assertIn("Terra", self.db.all_locations)
            self.assertNotIn("Earth", self.db.all_locations)
            self.assertEqual(self.db.all_locations["Terra"].location_type, "Home")

        def test_edit_nonexistent_location(self):
            """Test that editing a non-existent location fails."""
            result = self.db.edit_location("Jupiter", new_name="Big Jupiter")
            self.assertFalse(result)


    class TestRoute(unittest.TestCase):
        """Test the Route class."""

        def setUp(self):
            """Set up locations for route testing."""
            self.earth = Location("Earth", "Planet", (0, 0, 0))
            self.mars = Location("Mars", "Planet", (10, 5, 2))
            self.jupiter = Location("Jupiter", "Planet", (30, 15, 8))

        def test_route_creation(self):
            """Test creating a route with locations."""
            route = Route([self.earth, self.mars])
            self.assertEqual(len(route.locations), 2)
            self.assertEqual(route.starting_location, self.earth)
            self.assertEqual(route.ending_location, self.mars)

        def test_empty_route(self):
            """Test creating an empty route."""
            route = Route([])
            self.assertIsNone(route.starting_location)
            self.assertIsNone(route.ending_location)

        def test_add_stop(self):
            """Test adding a stop to a route."""
            route = Route([self.earth, self.mars])
            route.add_stop(self.jupiter)
            self.assertEqual(len(route.locations), 3)
            self.assertEqual(route.ending_location, self.jupiter)

        def test_remove_stop(self):
            """Test removing a stop from a route."""
            route = Route([self.earth, self.mars, self.jupiter])
            result = route.remove_stop(1)
            self.assertTrue(result)
            self.assertEqual(len(route.locations), 2)

        def test_remove_invalid_stop(self):
            """Test that removing an invalid index fails."""
            route = Route([self.earth, self.mars])
            result = route.remove_stop(5)
            self.assertFalse(result)


    class TestIGPS(unittest.TestCase):
        # UNIT TESTS: IGPS class (Business Logic Layer)
        # Tests route creation, optimization algorithms, and calculations
        # Includes integration testing between IGPS and LocationsDatabase

        def setUp(self):
            """Set up IGPS with a database."""
            self.db = LocationsDatabase()
            self.igps = IGPS(self.db)

            # Add test locations
            self.earth = Location("Earth", "Planet", (0, 0, 0))
            self.mars = Location("Mars", "Planet", (10, 5, 2))
            self.jupiter = Location("Jupiter", "Planet", (30, 15, 8))

            self.db.add_location(self.earth)
            self.db.add_location(self.mars)
            self.db.add_location(self.jupiter)

        def test_calculate_distance_between_locations(self):
            """Test distance calculation between two Location objects."""
            distance = self.igps.calculate_distance_between(self.earth, self.mars)
            expected = np.sqrt(10**2 + 5**2 + 2**2)
            self.assertAlmostEqual(distance, expected, places=2)

        def test_calculate_distance_between_coordinates(self):
            """Test distance calculation between coordinate tuples."""
            distance = self.igps.calculate_distance_between((0, 0, 0), (3, 4, 0))
            self.assertAlmostEqual(distance, 5.0, places=2)

        def test_get_location_by_name(self):
            """Test retrieving a location by name."""
            loc = self.igps.get_location("Earth")
            self.assertEqual(loc, self.earth)

        def test_get_nonexistent_location(self):
            """Test that getting a non-existent location returns None."""
            result = self.igps.get_location("Neptune")
            self.assertIsNone(result)

        def test_create_route_valid(self):
            """Test creating a valid route."""
            route = self.igps.create_route(["Earth", "Mars"])
            self.assertIsNotNone(route)
            self.assertEqual(len(route.locations), 2)

        def test_create_route_insufficient_locations(self):
            """Test that creating a route with less than 2 locations fails."""
            route = self.igps.create_route(["Earth"])
            self.assertIsNone(route)

        def test_create_route_invalid_location(self):
            """Test that creating a route with invalid location fails."""
            route = self.igps.create_route(["Earth", "Neptune"])
            self.assertIsNone(route)

        def test_add_stop_optimization(self):
            """Test that adding a stop automatically optimizes its position in the middle."""
            # Create a route: Earth -> Jupiter (long distance)
            route = self.igps.create_route(["Earth", "Jupiter"])
            original_start = route.starting_location
            initial_distance = route.total_distance

            # Add Mars - it should be inserted between Earth and Jupiter for optimal distance
            self.igps.add_stop_to_route(route, "Mars")

            # Route should now be: Earth -> Mars -> Jupiter
            self.assertEqual(len(route.locations), 3)

            # Verify Mars is in the middle (optimal position)
            self.assertEqual(route.locations[1].name, "Mars")

            # Starting location must remain unchanged
            self.assertEqual(route.starting_location, original_start)
            self.assertEqual(route.locations[0].name, "Earth")

        def test_add_stop_preserves_start(self):
            """Test that adding a stop never changes the starting location."""
            # Create route: Mars -> Jupiter
            route = self.igps.create_route(["Mars", "Jupiter"])
            original_start = route.starting_location

            # Add Earth (which is at position 0,0,0 - closest to origin)
            # Even if Earth at start would be optimal, it should NOT become the start
            self.igps.add_stop_to_route(route, "Earth")

            # Starting location must still be Mars
            self.assertEqual(route.starting_location, original_start)
            self.assertEqual(route.locations[0].name, "Mars")

            # Earth should be inserted somewhere after Mars (position 1 or 2)
            earth_index = next(i for i, loc in enumerate(route.locations) if loc.name == "Earth")
            self.assertGreater(earth_index, 0, "New stop should not be at position 0")

        def test_add_stop_to_short_route(self):
            """Test adding a stop to a route with less than 2 locations."""
            route = Route([self.earth])
            result = self.igps.add_stop_to_route(route, "Mars")
            self.assertTrue(result)
            self.assertEqual(len(route.locations), 2)

        def test_validate_coordinates_valid(self):
            """Test that valid coordinates pass validation."""
            result = self.igps.validate_coordinates((1000, 200, 500))
            self.assertTrue(result)

        def test_validate_coordinates_exceeds_radius(self):
            """Test that coordinates beyond galaxy radius fail validation."""
            result = self.igps.validate_coordinates((60000, 0, 0))
            self.assertFalse(result)

        def test_validate_coordinates_exceeds_height(self):
            """Test that coordinates beyond galaxy height fail validation."""
            result = self.igps.validate_coordinates((1000, 600, 0))
            self.assertFalse(result)


    class TestMember(unittest.TestCase):
        """Test the Member class."""

        def test_member_creation(self):
            """Test creating a member."""
            member = Member("M001", "John Doe", "Earth", "Mars")
            self.assertEqual(member.member_id, "M001")
            self.assertEqual(member.name, "John Doe")
            self.assertEqual(member.home, "Earth")
            self.assertEqual(member.work, "Mars")

        def test_save_location(self):
            """Test saving a location to member's saved locations."""
            member = Member("M001", "John Doe")
            loc = Location("Favorite Spot", "Station", (100, 200, 300))
            member.save_location(loc)
            self.assertEqual(len(member.saved_locations), 1)
            self.assertIn(loc, member.saved_locations)

        def test_save_route(self):
            """Test saving a route to member's saved routes."""
            member = Member("M001", "John Doe")
            earth = Location("Earth", "Planet", (0, 0, 0))
            mars = Location("Mars", "Planet", (10, 5, 2))
            route = Route([earth, mars])
            member.save_route(route)
            self.assertEqual(len(member.saved_routes), 1)


    class TestSystemManager(unittest.TestCase):
        # INTEGRATION TESTS: SystemManager (Application Layer)
        # These tests verify that all 4 layers work together correctly:
        # (SystemManager) coordinates properly
        # (IGPS) performs calculations correctly
        # (LocationsDatabase) manages data correctly
        # (Domain Models) maintain state correctly

        def setUp(self):
            """Set up a fresh system manager for each test."""
            self.system = SystemManager()

        def test_register_member(self):
            """Test registering a new member."""
            member = self.system.register_member("M001", "John Doe", "Earth", "Mars")
            self.assertIsNotNone(member)
            self.assertIn("M001", self.system.members)

        def test_register_duplicate_member(self):
            """Test that registering a duplicate member ID fails."""
            self.system.register_member("M001", "John Doe")
            member2 = self.system.register_member("M001", "Jane Doe")
            self.assertIsNone(member2)

        def test_remove_member(self):
            """Test removing a member."""
            self.system.register_member("M001", "John Doe")
            result = self.system.remove_member("M001")
            self.assertTrue(result)
            self.assertNotIn("M001", self.system.members)

        def test_remove_nonexistent_member(self):
            """Test that removing a non-existent member fails."""
            result = self.system.remove_member("M999")
            self.assertFalse(result)

    # RUN TESTS
    print("=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)

    # Run all tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)

    print("\n" + "=" * 60)
    print("RUNNING EXAMPLE USAGE")
    print("=" * 60 + "\n")

    # EXAMPLE USAGE

    # Initialize system
    system = SystemManager()

    # Admin adds realistic Milky Way locations to database
    print("=== Administrator Adding Milky Way Locations ===")
    print(f"Galaxy specifications: {IGPS.GALAXY_RADIUS} LY radius, {IGPS.GALAXY_HEIGHT} LY height")
    print(f"Spacecraft specs: {IGPS.AVG_SPEED} LY/hr, {IGPS.FUEL_EFFICIENCY} LY/gal, {IGPS.TANK_CAPACITY} gal tank\n")

    # Solar System - approximately 27,000 LY from galactic center
    system.admin_add_location(Location("Solar System", "Star System", (23000, 250, 1000)))

    # Galactic Center
    system.admin_add_location(Location("Sagittarius A*", "Black Hole", (0, 0, 0)))

    # Alpha Centauri - closest star system to Solar System (~4.37 LY away)
    system.admin_add_location(Location("Alpha Centauri", "Star System", (23004, 250, 1001)))

    # Andromeda Station - fictional station in the outer rim
    system.admin_add_location(Location("Andromeda Station", "Space Station", (45000, 300, 2000)))

    # Orion Nebula region
    system.admin_add_location(Location("Orion Nebula", "Nebula", (24000, 100, -1500)))

    # Kepler Mining Colony - mid-rim location
    system.admin_add_location(Location("Kepler Colony", "Mining Station", (15000, -200, 500)))
    print()

    # Register a member
    print("=== Member Registration ===")
    member = system.register_member("M001", "Commander Sarah Chen", "Solar System", "Andromeda Station")
    print()

    # Test 1: Short local route (within tank capacity)
    print("=== Test 1: Local Route (Solar System to Alpha Centauri) ===")
    local_route = system.igps.create_route(["Solar System", "Alpha Centauri"])
    if local_route:
        system.igps.display_route_segments(local_route)
        system.igps.calculate_fuel_required(local_route)
        system.igps.calculate_travel_time(local_route)
    print()

    # Test 2: Longer route requiring refueling
    print("=== Test 2: Long Distance Route (Solar System to Andromeda Station) ===")
    long_route = system.igps.create_route(["Solar System", "Andromeda Station"])
    if long_route:
        system.igps.calculate_fuel_required(long_route)
        system.igps.calculate_travel_time(long_route)
    print()

    # Test 3: Multi-stop optimized route
    print("=== Test 3: Multi-Stop Optimized Route ===")
    multi_route = system.igps.optimize_route([
        "Solar System",
        "Alpha Centauri",
        "Orion Nebula",
        "Kepler Colony"
    ])
    if multi_route:
        print("Route order:", " -> ".join([loc.name for loc in multi_route.locations]))
        system.igps.display_route_segments(multi_route)
        system.igps.calculate_fuel_required(multi_route)
        system.igps.calculate_travel_time(multi_route)
    print()

    # Test 4: Adding a stop with automatic optimization
    print("=== Test 4: Adding Stop with Automatic Optimization ===")
    print("Creating route: Solar System -> Orion Nebula -> Kepler Colony")
    test_route = system.igps.create_route(["Solar System", "Orion Nebula", "Kepler Colony"])
    if test_route:
        print(f"Initial distance: {system.igps.format_distance(test_route.total_distance)}")
        print("Initial route order:", " -> ".join([loc.name for loc in test_route.locations]))
        print("\nAdding Alpha Centauri to route (will find optimal position, but won't change start)...")
        system.igps.add_stop_to_route(test_route, "Alpha Centauri")
        print("Final route order:", " -> ".join([loc.name for loc in test_route.locations]))
        print(f"Note: Starting location '{test_route.locations[0].name}' remains unchanged")
        system.igps.display_route_segments(test_route)
    print()

    # Test 5: Random exploration route with new planets
    print("=== Test 5: Exploration Route (New Planets) ===")
    print("Adding three new planets to the database...")

    # Add three planets with specific names
    # Planet in the inner rim
    system.admin_add_location(Location("Evil_Planet", "Exoplanet", (8000, -150, 3000)))

    # Planet in the outer rim
    system.admin_add_location(Location("Glibglob", "Colony World", (42000, 400, -8000)))

    # Planet near the galactic center
    system.admin_add_location(Location("Innocent_Planet", "Research Station", (5000, 100, -2000)))

    print("\nCreating exploration route: Evil_Planet -> Glibglob -> Innocent_Planet")
    exploration_route = system.igps.optimize_route(["Evil_Planet", "Glibglob", "Innocent_Planet"])
    if exploration_route:
        print("Optimized route order:", " -> ".join([loc.name for loc in exploration_route.locations]))
        system.igps.display_route_segments(exploration_route)
        system.igps.calculate_fuel_required(exploration_route)
        system.igps.calculate_travel_time(exploration_route)
    print()

    # Save route for member
    print("=== Saving Route for Member ===")
    member.save_route(multi_route)
    member.save_location(Location("Favorite Rest Stop", "Station", (25000, 200, 800)))
    print(f"Member {member.name} has {len(member.saved_routes)} saved route(s)")
    print(f"Member {member.name} has {len(member.saved_locations)} saved location(s)")
    print()

    # 3D VISUALIZATION
    print("=" * 60)
    print("CREATING 3D ROUTE VISUALIZATION")
    print("=" * 60 + "\n")

    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        # Create figure with subplots for multiple routes (now 2x3 grid)
        fig = plt.figure(figsize=(20, 12))

        # Plot 1: Local Route (Solar System to Alpha Centauri)
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        if local_route:
            # Extract coordinates
            x_coords = []
            y_coords = []
            z_coords = []
            names = []

            for loc in local_route.locations:
                if isinstance(loc, Location):
                    x_coords.append(loc.position[0])
                    y_coords.append(loc.position[2])  # Z becomes Y (up/down)
                    z_coords.append(loc.position[1])  # Y becomes Z (depth)
                    names.append(loc.name)
                else:
                    x_coords.append(loc[0])
                    y_coords.append(loc[2])
                    z_coords.append(loc[1])
                    names.append(f"({loc[0]}, {loc[1]}, {loc[2]})")

            # Plot the route as a line
            ax1.plot(x_coords, y_coords, z_coords, 'b-', linewidth=2, label='Route Path')
            # Plot the waypoints
            ax1.scatter(x_coords, y_coords, z_coords, c='red', s=100, marker='o')
            # Label each point
            for i, name in enumerate(names):
                ax1.text(x_coords[i], y_coords[i], z_coords[i], f'  {name}', fontsize=8)

            ax1.set_xlabel('X (Light Years)')
            ax1.set_ylabel('Z (Light Years) - Height')
            ax1.set_zlabel('Y (Light Years) - Depth')
            ax1.set_title('Local Route:\nSolar System → Alpha Centauri')
            ax1.legend()

        # Plot 2: Long Distance Route
        ax2 = fig.add_subplot(2, 3, 2, projection='3d')
        if long_route:
            x_coords = []
            y_coords = []
            z_coords = []
            names = []

            for loc in long_route.locations:
                if isinstance(loc, Location):
                    x_coords.append(loc.position[0])
                    y_coords.append(loc.position[2])  # Z becomes Y (up/down)
                    z_coords.append(loc.position[1])  # Y becomes Z (depth)
                    names.append(loc.name)

            ax2.plot(x_coords, y_coords, z_coords, 'g-', linewidth=2, label='Route Path')
            ax2.scatter(x_coords, y_coords, z_coords, c='orange', s=100, marker='o')
            for i, name in enumerate(names):
                ax2.text(x_coords[i], y_coords[i], z_coords[i], f'  {name}', fontsize=8)

            ax2.set_xlabel('X (Light Years)')
            ax2.set_ylabel('Z (Light Years) - Height')
            ax2.set_zlabel('Y (Light Years) - Depth')
            ax2.set_title('Long Distance Route:\nSolar System → Andromeda Station')
            ax2.legend()

        # Plot 3: Multi-Stop Optimized Route
        ax3 = fig.add_subplot(2, 3, 3, projection='3d')
        if multi_route:
            x_coords = []
            y_coords = []
            z_coords = []
            names = []

            for loc in multi_route.locations:
                if isinstance(loc, Location):
                    x_coords.append(loc.position[0])
                    y_coords.append(loc.position[2])  # Z becomes Y (up/down)
                    z_coords.append(loc.position[1])  # Y becomes Z (depth)
                    names.append(loc.name)

            ax3.plot(x_coords, y_coords, z_coords, 'm-', linewidth=2, label='Optimized Route')
            ax3.scatter(x_coords, y_coords, z_coords, c='purple', s=100, marker='o')
            for i, name in enumerate(names):
                ax3.text(x_coords[i], y_coords[i], z_coords[i], f'  {name}', fontsize=7)

            ax3.set_xlabel('X (Light Years)')
            ax3.set_ylabel('Z (Light Years) - Height')
            ax3.set_zlabel('Y (Light Years) - Depth')
            ax3.set_title('Multi-Stop Optimized Route:\n' + ' → '.join(names))
            ax3.legend()

        # Plot 4: Route with Added Stop (showing optimization)
        ax4 = fig.add_subplot(2, 3, 4, projection='3d')
        if test_route:
            x_coords = []
            y_coords = []
            z_coords = []
            names = []

            for loc in test_route.locations:
                if isinstance(loc, Location):
                    x_coords.append(loc.position[0])
                    y_coords.append(loc.position[2])  # Z becomes Y (up/down)
                    z_coords.append(loc.position[1])  # Y becomes Z (depth)
                    names.append(loc.name)

            ax4.plot(x_coords, y_coords, z_coords, 'c-', linewidth=2, label='Route with Added Stop')
            ax4.scatter(x_coords, y_coords, z_coords, c='cyan', s=100, marker='o')
            for i, name in enumerate(names):
                ax4.text(x_coords[i], y_coords[i], z_coords[i], f'  {name}', fontsize=7)

            ax4.set_xlabel('X (Light Years)')
            ax4.set_ylabel('Z (Light Years) - Height')
            ax4.set_zlabel('Y (Light Years) - Depth')
            ax4.set_title('Route with Optimized Stop:\n' + ' → '.join(names))
            ax4.legend()

        # Plot 5: Exploration Route (NEW!)
        ax5 = fig.add_subplot(2, 3, 5, projection='3d')
        if exploration_route:
            x_coords = []
            y_coords = []
            z_coords = []
            names = []

            for loc in exploration_route.locations:
                if isinstance(loc, Location):
                    x_coords.append(loc.position[0])
                    y_coords.append(loc.position[2])  # Z becomes Y (up/down)
                    z_coords.append(loc.position[1])  # Y becomes Z (depth)
                    names.append(loc.name)

            ax5.plot(x_coords, y_coords, z_coords, 'r-', linewidth=2.5, label='Exploration Route')
            ax5.scatter(x_coords, y_coords, z_coords, c='lime', s=120, marker='^', edgecolors='darkgreen', linewidths=2)
            for i, name in enumerate(names):
                ax5.text(x_coords[i], y_coords[i], z_coords[i], f'  {name}', fontsize=8, weight='bold')

            ax5.set_xlabel('X (Light Years)')
            ax5.set_ylabel('Z (Light Years) - Height')
            ax5.set_zlabel('Y (Light Years) - Depth')
            ax5.set_title('Random Exploration Route:\n' + ' → '.join(names))
            ax5.legend()

        # Plot 6: All routes comparison overlay
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')

        # Plot all routes on one graph for comparison
        routes_to_plot = [
            (local_route, 'blue', 'o', 'Local Route'),
            (long_route, 'green', 's', 'Long Distance'),
            (multi_route, 'purple', 'D', 'Multi-Stop'),
            (exploration_route, 'red', '^', 'Exploration')
        ]

        for route, color, marker, label in routes_to_plot:
            if route:
                x_coords = []
                y_coords = []
                z_coords = []

                for loc in route.locations:
                    if isinstance(loc, Location):
                        x_coords.append(loc.position[0])
                        y_coords.append(loc.position[2])  # Z becomes Y
                        z_coords.append(loc.position[1])  # Y becomes Z

                ax6.plot(x_coords, y_coords, z_coords, color=color, linewidth=1.5, alpha=0.7)
                ax6.scatter(x_coords, y_coords, z_coords, c=color, s=80, marker=marker, label=label, alpha=0.8)

        ax6.scatter([0], [0], [0], c='black', s=200, marker='X', label='Galactic Center')
        ax6.set_xlabel('X (Light Years)')
        ax6.set_ylabel('Z (Light Years) - Height')
        ax6.set_zlabel('Y (Light Years) - Depth')
        ax6.set_title('All Routes Comparison')
        ax6.legend(fontsize=8)
        ax6.view_init(elev=25, azim=45)

        plt.tight_layout()
        plt.savefig('igps_routes_3d.png', dpi=150, bbox_inches='tight')
        print("3D visualization saved as 'igps_routes_3d.png'")
        plt.show()

        # Create a single comprehensive view showing all locations
        fig2 = plt.figure(figsize=(14, 10))
        ax_all = fig2.add_subplot(111, projection='3d')

        # Plot all locations in the database
        all_x = []
        all_y = []
        all_z = []
        all_names = []

        for name, loc in system.database.all_locations.items():
            all_x.append(loc.position[0])
            all_y.append(loc.position[2])  # Z becomes Y (up/down) - galaxy height
            all_z.append(loc.position[1])  # Y becomes Z (depth)
            all_names.append(name)

        # Scatter plot all locations
        ax_all.scatter(all_x, all_y, all_z, c='gold', s=150, marker='*',
                      label='Galaxy Locations', edgecolors='black', linewidths=1)

        # Label each location
        for i, name in enumerate(all_names):
            ax_all.text(all_x[i], all_y[i], all_z[i], f'  {name}', fontsize=9, weight='bold')

        # Overlay the multi-stop route
        if multi_route:
            route_x = [loc.position[0] for loc in multi_route.locations if isinstance(loc, Location)]
            route_y = [loc.position[2] for loc in multi_route.locations if isinstance(loc, Location)]  # Z -> Y
            route_z = [loc.position[1] for loc in multi_route.locations if isinstance(loc, Location)]  # Y -> Z
            ax_all.plot(route_x, route_y, route_z, 'r-', linewidth=3, label='Sample Route', alpha=0.7)

        # Add galactic center marker
        ax_all.scatter([0], [0], [0], c='black', s=300, marker='X', label='Galactic Center')

        ax_all.set_xlabel('X (Light Years)', fontsize=11)
        ax_all.set_ylabel('Z (Light Years) - Height', fontsize=11)
        ax_all.set_zlabel('Y (Light Years) - Depth', fontsize=11)
        ax_all.set_title('Milky Way Galaxy - All Locations and Sample Route', fontsize=14, weight='bold')
        ax_all.legend(fontsize=10)

        # Set viewing angle
        ax_all.view_init(elev=20, azim=45)

        plt.savefig('igps_galaxy_map.png', dpi=150, bbox_inches='tight')
        print("✓ Galaxy map saved as 'igps_galaxy_map.png'")
        plt.show()

        print("\n✓ All visualizations generated successfully!")

    except ImportError:
        print("⚠ Matplotlib not available. Install with: pip install matplotlib")
        print("  Visualization skipped, but all other functionality works fine.")
