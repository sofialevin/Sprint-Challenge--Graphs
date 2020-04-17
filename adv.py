from room import Room
from player import Player
from world import World
from util import Stack, Queue

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

# helper function for getting opposite direction
def opposite(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'

prev_room = None
rooms = set()
stack = []
# path for going backwards
back_path = []
visited = {
    player.current_room.id: {}
}

# set up stack and back_path with an initial direction
directions = player.current_room.get_exits()
current_direction = directions[0]
stack.append(current_direction)
back_path.append(opposite(current_direction))

# create directions in initial room
for direction in directions:
    visited[player.current_room.id][direction] = "?"

while len(visited) < len(room_graph):
    prev_room = player.current_room.id
    current_direction = stack[-1]
    player.travel(current_direction)
    traversal_path.append(current_direction)
    rooms.add(player.current_room.id)

    # when moving between rooms update the previous room with the direction travelled
    visited[prev_room][current_direction] = player.current_room.id

    if player.current_room.id not in visited:
        # add new room to visited
        visited[player.current_room.id] = {}
    if prev_room is not None:
        # when moving between rooms update the current room with the direction travelled
        visited[player.current_room.id][opposite(current_direction)] = prev_room

    # make list with possible moves
    possible_directions = []
    for direction in player.current_room.get_exits():
        if direction not in visited[player.current_room.id]:
            visited[player.current_room.id][direction] = "?"
        if visited[player.current_room.id][direction] is "?":
            possible_directions.append(direction)

    # if possible moves exist, pick one and add to stack. also update back_path.
    if len(possible_directions) > 0:
        stack.append(possible_directions[0])
        back_path.append(opposite(possible_directions[0]))
    else:
        # if no possible moves exist, add previous room from back_path to stack
        back = back_path.pop()
        stack.append(back)



# TRAVERSAL TEST
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
