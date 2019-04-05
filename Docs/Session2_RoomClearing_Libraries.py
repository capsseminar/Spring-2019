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
