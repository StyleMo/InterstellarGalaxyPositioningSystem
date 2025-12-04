from src.models import Member
from src.database import LocationsDatabase
from src.igps import IGPS


class SystemManager:
    """APPLICATION LAYER: SystemManager sits at the top of the architecture"""
    
    def __init__(self):
        self.members = {}  # Dictionary for O(1) lookup
        self.database = LocationsDatabase()  # Data Access Layer
        self.igps = IGPS(self.database)  # Business Logic Layer

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
