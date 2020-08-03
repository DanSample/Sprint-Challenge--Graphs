from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Get all the exits with the room.
# Move in one direction, add to the traversal path, pop it off the directions for the room
# Figure out opposite direction, add this to the backtracking path and remove the opposite direction from the unexplored paths
# Get exits for the new room and keep track of it (in visited)
# Move in a random direction, add to the traversal path and pop it off the possible directions
# Keep moving until you reach an end
# If there are no more unexplored exits, backtrack along the last direction on the backtracking path 
# and remove it, add to the traversal path
# Check that room for unexplored directions and repeat 
# Keep going until the number of rooms visited reaches the length of the rooms graph

def the_paths(direction):

    # Set up the directions for backtracking

    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"

# Create a Stack and a set
paths = Stack()
visited = set()

# while the length of visited is less than the length of the rooms
while len(visited) < len(world.rooms):
    # Create an exit variable and path(list)
    exits = player.current_room.get_exits()
    path = []

    # Iterate over the exits
    for exit in exits:
        # If the exit is not None and get room in direction (exit) is not in visited
        if exit is not None and player.current_room.get_room_in_direction(exit) not in visited:
            # Append the exit to the path
            path.append(exit)
    # Then add the current room to visited
    visited.add(player.current_room)

    # If the length of the path is greater than zero.
    if len(path) > 0:
        # Create a variable to randomly move
        move = random.randint(0, len(path) -1)
        # Push the path with move into the Stack (paths)
        paths.push(path[move])
        # Move (travel) the player with move 
        player.travel(path[move])
        # Append the path to the traversal path
        traversal_path.append(path[move])

    # Else
    else:
        # Create a variable to pop off the paths
        end = paths.pop()
        # Move (travel) the paths with the end
        player.travel(the_paths(end))
        # Append the paths(end) to the traversal path
        traversal_path.append(the_paths(end))





# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
