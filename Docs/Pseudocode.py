### LIBRARIES
import locomotion as lm # Enables high-level control over bot movement
import visual_cortex as vc # Enables high-level control over optical sensors
import geo_map as gm # Enables tracking of relative position and cardinal direction
from lm import left, right, forward, back # Controls turns and forward/back movement
from vc import human_detect, mine_detect, door_detect # The code only looks for these three objects
from gm import cardinal_direction, rel_position # Records direction and position relative to starting point


### MODULES

## visual_cortex

def scan(self, refresh = 1):
	frontSensor_input = dataCollect(frontSensor, refresh) # "dataCollect" is a primitive function that collects data from the front camera sensor
	image = process(frontSensor_input, refresh) # 1 is in units of seconds; "process" is a primitive image processing function

def detect(image):
	matched_object = match(image) # "match" is a primitive function that maps images to stored objects
	if matched_object == human:
		human_detected = TRUE
	if matched_object == mine:
		mine_detected = TRUE
	if matched_object == door:
		door_detect = TRUE

## locomotion

# "rotate" is a primite function and "degrees" is defined
def turn_right(self, degrees = 90): # This sets the default value of "degrees" to 90
	self.rotate(degrees)
	break

def turn_left(self, degrees = -90):
	self.rotate(degrees)
	break

def move_forward(self, distance = 1.5): # Units are coded to be in meters
	while door_detect == TRUE:
		wheel.rotate(1) # Positive numbers are coded to move "forward"
		distance_counter = distance_counter + 1
		if human_detect == TRUE:
			stop()
			commander.radio("HUMAN") # Send commander radio message; "radio" is primitive
		if mine_detect == TRUE:
			stop()
			commander.radio("MINE") # Send commander radio message; "radio" is primitive
	wheel.rotate(distance / 6.28*wheel_diameter) # "wheel_diameter" is a defined value
	distance_counter = distance_counter + (distance / 6.28*wheel_diameter)

def move_backward(self, distance = -1.5): # Units are coded to be in meters
	while door_detect == TRUE:
		wheel.rotate(-1) # Positive numbers are coded to move "forward"
		distance_counter = distance_counter + 1
		if human_detect == TRUE:
			stop()
			commander.radio("HUMAN") # Send commander radio message; "radio" is primitive
		if mine_detect == TRUE:
			stop()
			commander.radio("MINE") # Send commander radio message; "radio" is primitive
	wheel.rotate(distance / 6.28*wheel_diameter) # "wheel_diameter" is a defined value
	distance_counter = distance_counter + (distance / 6.28*wheel_diameter)

def stop(self): # Causes all movement to cease
	turn_right(self, 0)
	turn_left(self, 0)
	move_forward(self, 0)
	move_back(self, 0)

def end_mission(self):
	kill_switch = FALSE
	if bot.radio("END"): # If commander sends bot radio signal to "END"; "radio" is primitive
		kill_switch = TRUE

## geo_map

def cardinal_direction(refresh = 1): # "refresh" is in units of seconds; 
	if system.clock() % refresh == 0: # Function is true whenever time reach a whole unit of specified seconds; "system.clock" is a primitive function
		card_dir = direction.get(frontSensor_input) # "direction" is an included dictionary of N, E, S, W

def rel_position(refresh):
	if system.clock() % refresh == 0: # Function is true whenever time reach a whole unit of specified seconds; "system.clock" is a primitive function
		rel_pos = trigonometry(cardinal_direction, distanceCounter) # A primitive function that determines distance from these two variables

def check_visited(rel_pos):
	if door_detect == TRUE:
		for door_pos in visited_doors:
			if rel_pos == door_pos: # Checks whether the current position has already been visited
				door_detect = FALSE # If it has been visited, ignores the door detection and moves on
				break

				
### MAIN SCRIPT

## Assume a starting position of facing forward in the front door

# System startup
mission_active = TRUE # Initiates robot mission
distance_counter = 0 # Starts a distance counter used for relative positioning
visited_doors = () # This will become a list of visited doors, recorded by position seen
start_time = system.clock() # Runs the system clock once on startup to set initial time

# Human input
time_limit = raw_input("What is the maximum time to search, in hours?") * 3600 # Gives the bot a time limit in seconds

# Basic functions startup

# Procedure
turn_right() # Begins with an initial turn
while mission_active == TRUE: # Sets to continually run mission until this variable is changed to FALSE
	if kill_switch == TRUE: # Allows the commander to remotely stop the mission
		stop() # Stops all movement
		mission_active = FALSE # Ends while loop and therefore all activity
		break
	if system_clock() - start_time > time_limit: # Stops the mission after a specified time limit
		mission_active = FALSE # Ends while loop and therefore all activity
		break
	else:
		scan() # Activates image processing repeatedly every specified unit of time, looking for doors, humans, and mines
		detect() # Begins the image processing function, which runs continuously 
		if human_detect == TRUE:
			stop()
			commander.radio("HUMAN") # Send commander radio message; "radio" is primitive
		if mine_detect == TRUE:
			stop()
			commander.radio("MINE") # Send commander radio message; "radio" is primitive
		if door_detect == TRUE:
			check_visited(rel_pos) # If the door has already been visited, door_detect will become FALSE and the bot will ignore the door and move on
			visited_doors.append(rel_pos) # If the door was not yet visited, this adds the position from which the door was detected to the visited doors list
			move_forward() # The bot moves toward the door and then a specified distance beyond it (to fully enter the room)
		else:
			turn_left()
		continue # Returns the code to the "while mission_active == TRUE" line


### Potential issues implanted into the code (intentional - many uninentional ones will also appear):
###
### The turn_right and turn_left functions turn the bot 90 degrees by default.
### The move_forward function moves the bot 1 meter into a new room by default.
### The direction tracker only takes one of four values (N, E, S, W).
### The image detection mechanisms are unknown and buried in further code.
### The functions to radio in human or mine detection are buried within the
###     locomotion functions, rather than being accessible in the main script.
### The bot can only detect humans and mines when moving forward and backward,
###     not when turning (or staying still, though it is never coded to stay still).
### It is difficult to guarantee that a door will be seen from the same position,
###     so many doors many be counted more than once (possibly many more times).
### The move_backward function is never used, making its inclusion somewhat
###     suspicious: was it intended to be used, or included? May signal more issues.
### Time limit entry is open to human input error.
### While the mission has a time limit and can be ended via radio input at any time,
###     the program has no provision for deciding all rooms have been checked!
###     How might we add this functionality?
