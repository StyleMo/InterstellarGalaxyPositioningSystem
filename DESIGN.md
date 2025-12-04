Design - Metrics
Distance is measured in LightYears (LY). 
The average Spacecraft is expected to be able to travel 50-100LY per hour. 
The average Spacecraft is expected to have 250LY per gallon of fuel. (15 Gallon Average). 
The actual MilkyWay Galaxy is about 100,000LY in diameter with a width of 1000LY. The speed to travel the Galaxy with this system would be roughly the same as travelling Earth with a car. 

Design - OOP Classes
Location Class - These objects can be any major location in the Milky Way, such as Planets and Stars. 
Location Database - Our main Location Database holds all of the locations in the Galaxy. 
Route - Created Route Objects find the shortest distance between two Locations. 
User and Member - Users and Members interact with the IGPS system to create and save routes between locations. 
System Management - Handles monitoring and changing the Database and Users/Members. 
IGPS - Does the heavy lifting for the system. This is the class that creates and modifies the routes between locations, and interracts with the users/members/database and management. 

Design Patterns and Architecture
The current back end design is done with Layered Architecture. 
Location Database | Modify Locations | Modifying Database | Location Validation
Route Creation | Route Modification | Distance Calculations | Distance Optimizations
Creating Members | Managing Membership | Membership Data | Secure Members | Administration

The fully completed software will implement the Model View Controller pattern (MVC) to handle working with the front end (UI), back end (Computations), and the Database (input validation). 

Key Testing Design and Edge Cases
Database can’t add the same Location twice. 
Removing/Editing a nonexistent location should fail. 
Non-Existent Locations should return none when searched. 
Empty Routes should return none. 
Make sure calculated Distances are Correct. 
IGPS should not return a location not added yet. 
Routes of only 1 location can’t be created. 
Creating a route with a Location not in the Database will fail. 
A new added location can never be the starting location. 
Assert that Invalid coordinates will be out of bounds. 
Other tests verify that the created methods work. 

Design Reflection and Future
Overall the IGPS is going as planned, and users are quickly being able to generate the routes. 
Reflection - Despite having the entire OOP system planned ahead of time, the development did have unexpected complications, or required additions that weren’t initially planned for. 
This could include optimizing the route once a new route is added, and general interactions between the classes. 
It’s also important to realize what classes need objects to be created versus which ones don’t. This was not originally accounted for. I ended up making both the Database and IGPS run through the system itself, while members and locations are created objects. These are important things to keep in mind during the design phase. 
The advantage of the split OOP approach is that it is easy for me to add new features, such as the route optimization mentioned above, and can even implement event-driven programming easily with the existing structure. This will be helpful with developing the front-end. 


