    IGPS Overview
	Have you ever wanted to know the best route to go from Earth, to the Sun, to Pluto, and then to the nearest Black Hole? This project has got you covered! 
	This project will be making the debut of the ever-desired Intergalactic Positioning System (also known as the IGPS). This system will allow users and members alike to get the fastest routes between their starting and ending locations, as well as make stops in between. All stops are calculated to give the fastest distance. Naturally this also means that the IGPS can display the positioning of a certain location in the case a user just wants to know where it is. 
	The System will have an integrated database called the Galaxy Locations Database, which stores all key locations in the MilkyWay Galaxy, and this database will be used to access the locations of known existing locations in the galaxy. Administrators would be in charge of updating the GLD, unless an automated system were to be created at some point. 
For the sake of this project, not every location in the galaxy is going to be added, but there WILL be a standardized system for pathfinding, as well as actual example locations for the final product. An easy way to think of this project is that it would be very similar to a Sea GPS system, but at a Space-Scale. 
While not relevant to Stage 1, it’s important to note that there are some key standardizations that will be important for the testing stages. 

Distance is measured in LightYears (LY). 
The average Spacecraft is expected to be able to travel 50-100LY per hour. 
The average Spacecraft is expected to have 25LY per gallon of fuel. (15 Gallon Average). 
The actual MilkyWay Galaxy is about 100,000LY in diameter. The speed to travel the Galaxy with this system would be roughly the same as travelling Earth with a car. 

	If you think these standardizations are made up, just watch the news. Regardless, the final project WILL meet all of the functional requirements, and the standardizations above could be changed to match 
	that. In fact, they could simply be Earth-level standardizations and it would be similar to a Sea GPS, but that already exists, this doesn’t. 

FUNCTIONAL DEPENDENCIES
The IGPS will give users and members a route between all desired locations that covers the least amount of calculated distance. 
The distance between two locations in the route, or two entered locations are given to the user/member at request. 
A user can register to become a member by entering the required information. 
The IGPS must be able to calculate the amount of fuel required for the trip and display it at user/member request. 
The system will not create a route upon input of a named location that does not exist in the Galaxy Locations Database. 
A member can save a route, and also save individual locations. 
The IGPS will display the position of a specific location upon user request. 
A member can set a certain location as their home or work location. 
A saved or set location from a member need not be a named location in the database, but unnamed locations must have user-input coordinates. 
An administrator can update the Galaxy Locations Database to add new locations, edit existing locations, and delete locations. 
Users/Members have the option to enter a named location (see requirement 5), or enter exact coordinates to count as a location. 
Users/Members will be able to modify the routes by adding/removing locations to the route. 

USAGE EXAMPLES
“As an Alien Overlord, I want an application that gives me the shortest route to all of the planets I aim to visit so that I can destroy all the target planets while spending as little fuel as possible!” 

“As a Space Cargo Transport, I need the fastest route to my drop off locations, so I can get my job done as quickly as possible.” 

“As a frugal Space Traveller I would like to know the distance and fuel requirement to get to my destination, so I can plan any appropriate fuel stops, while also limiting as many fuel stops as possible.” 

“I often want to go far off into the Galaxy, but I want to have some method to track back home so I don’t get lost!” 
