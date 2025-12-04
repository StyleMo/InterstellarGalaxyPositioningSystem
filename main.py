from src.models import Location
from src.system_manager import SystemManager
from src.igps import IGPS


def main():
    # Initialize system
    system = SystemManager()

    # Admin adds realistic Milky Way locations to database
    print("=" * 60)
    print("IGPS - INTELLIGENT GALAXY POSITIONING SYSTEM")
    print("=" * 60)
    print("\n=== Administrator Adding Milky Way Locations ===")
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
    system.admin_add_location(Location("Evil_Planet", "Exoplanet", (8000, -150, 3000)))
    system.admin_add_location(Location("Glibglob", "Colony World", (42000, 400, -8000)))
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

        # Create figure with subplots for multiple routes (2x3 grid)
        fig = plt.figure(figsize=(20, 12))

        routes_to_visualize = [
            (local_route, "Local Route:\nSolar System → Alpha Centauri", 1, 'blue', 'red'),
            (long_route, "Long Distance Route:\nSolar System → Andromeda Station", 2, 'green', 'orange'),
            (multi_route, "Multi-Stop Optimized Route", 3, 'magenta', 'purple'),
            (test_route, "Route with Optimized Stop", 4, 'cyan', 'cyan'),
            (exploration_route, "Random Exploration Route", 5, 'red', 'lime')
        ]

        for route, title, position, line_color, point_color in routes_to_visualize:
            if route:
                ax = fig.add_subplot(2, 3, position, projection='3d')
                
                x_coords = []
                y_coords = []
                z_coords = []
                names = []

                for loc in route.locations:
                    if isinstance(loc, Location):
                        x_coords.append(loc.position[0])
                        y_coords.append(loc.position[2])  # Z becomes Y (up/down)
                        z_coords.append(loc.position[1])  # Y becomes Z (depth)
                        names.append(loc.name)

                ax.plot(x_coords, y_coords, z_coords, f'{line_color[0]}-', linewidth=2, label='Route Path')
                ax.scatter(x_coords, y_coords, z_coords, c=point_color, s=100, marker='o')
                
                for i, name in enumerate(names):
                    ax.text(x_coords[i], y_coords[i], z_coords[i], f'  {name}', fontsize=7)

                ax.set_xlabel('X (Light Years)')
                ax.set_ylabel('Z (Light Years) - Height')
                ax.set_zlabel('Y (Light Years) - Depth')
                
                if position == 3 and multi_route:
                    full_title = title + ":\n" + ' → '.join(names)
                    ax.set_title(full_title)
                elif position == 5 and exploration_route:
                    full_title = title + ":\n" + ' → '.join(names)
                    ax.set_title(full_title)
                else:
                    ax.set_title(title)
                ax.legend()

        # Plot 6: All routes comparison overlay
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')

        routes_overlay = [
            (local_route, 'blue', 'o', 'Local Route'),
            (long_route, 'green', 's', 'Long Distance'),
            (multi_route, 'purple', 'D', 'Multi-Stop'),
            (exploration_route, 'red', '^', 'Exploration')
        ]

        for route, color, marker, label in routes_overlay:
            if route:
                x_coords = [loc.position[0] for loc in route.locations if isinstance(loc, Location)]
                y_coords = [loc.position[2] for loc in route.locations if isinstance(loc, Location)]
                z_coords = [loc.position[1] for loc in route.locations if isinstance(loc, Location)]

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
        print("✓ 3D visualization saved as 'igps_routes_3d.png'")

        # Create a single comprehensive view showing all locations
        fig2 = plt.figure(figsize=(14, 10))
        ax_all = fig2.add_subplot(111, projection='3d')

        all_x = []
        all_y = []
        all_z = []
        all_names = []

        for name, loc in system.database.all_locations.items():
            all_x.append(loc.position[0])
            all_y.append(loc.position[2])
            all_z.append(loc.position[1])
            all_names.append(name)

        ax_all.scatter(all_x, all_y, all_z, c='gold', s=150, marker='*',
                      label='Galaxy Locations', edgecolors='black', linewidths=1)

        for i, name in enumerate(all_names):
            ax_all.text(all_x[i], all_y[i], all_z[i], f'  {name}', fontsize=9, weight='bold')

        if multi_route:
            route_x = [loc.position[0] for loc in multi_route.locations if isinstance(loc, Location)]
            route_y = [loc.position[2] for loc in multi_route.locations if isinstance(loc, Location)]
            route_z = [loc.position[1] for loc in multi_route.locations if isinstance(loc, Location)]
            ax_all.plot(route_x, route_y, route_z, 'r-', linewidth=3, label='Sample Route', alpha=0.7)

        ax_all.scatter([0], [0], [0], c='black', s=300, marker='X', label='Galactic Center')

        ax_all.set_xlabel('X (Light Years)', fontsize=11)
        ax_all.set_ylabel('Z (Light Years) - Height', fontsize=11)
        ax_all.set_zlabel('Y (Light Years) - Depth', fontsize=11)
        ax_all.set_title('Milky Way Galaxy - All Locations and Sample Route', fontsize=14, weight='bold')
        ax_all.legend(fontsize=10)
        ax_all.view_init(elev=20, azim=45)

        plt.savefig('igps_galaxy_map.png', dpi=150, bbox_inches='tight')
        print("✓ Galaxy map saved as 'igps_galaxy_map.png'")
        plt.show()

        print("\n✓ All visualizations generated successfully!")

    except ImportError:
        print("⚠ Matplotlib not available. Install with: pip install matplotlib")
        print("  Visualization skipped, but all other functionality works fine.")

    print("\n" + "=" * 60)
    print("IGPS DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
