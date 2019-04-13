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
		# At this point the code rerturns to the "while mission_active == TRUE" line
    
### What are potential issues in this hard-coded procedure?
### (It includes many intentional issues - bonus points for finding unintentional ones!)
