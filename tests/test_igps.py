import unittest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Location, Route, Member
from src.database import LocationsDatabase
from src.igps import IGPS
from src.system_manager import SystemManager


class TestLocation(unittest.TestCase):
    """UNIT TESTS: Location class - Tests basic CRUD operations and data integrity"""

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
    """UNIT TESTS: LocationsDatabase class (Data Access Layer)"""

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
        """ERROR HANDLING TEST: Adding duplicate location should fail"""
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
    """UNIT TESTS: IGPS class (Business Logic Layer)"""

    def setUp(self):
        """Set up IGPS with a database."""
        self.db = LocationsDatabase()
        self.igps = IGPS(self.db)

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
        route = self.igps.create_route(["Earth", "Jupiter"])
        original_start = route.starting_location

        self.igps.add_stop_to_route(route, "Mars")

        self.assertEqual(len(route.locations), 3)
        self.assertEqual(route.locations[1].name, "Mars")
        self.assertEqual(route.starting_location, original_start)
        self.assertEqual(route.locations[0].name, "Earth")

    def test_add_stop_preserves_start(self):
        """Test that adding a stop never changes the starting location."""
        route = self.igps.create_route(["Mars", "Jupiter"])
        original_start = route.starting_location

        self.igps.add_stop_to_route(route, "Earth")

        self.assertEqual(route.starting_location, original_start)
        self.assertEqual(route.locations[0].name, "Mars")

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
    """INTEGRATION TESTS: SystemManager (Application Layer)"""

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
