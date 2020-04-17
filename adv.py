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

visited = {}
prev_room = None

rooms = set()

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

visited = {0: {'n': '?', 's': '?', 'e': '?', 'w': '?'}}

directions = player.current_room.get_exits()
current_direction = directions[0]

unexplored_rooms = len(room_graph)

while unexplored_rooms > 0:
    prev_room = player.current_room.id
    player.travel(current_direction)
    traversal_path.append(current_direction)
    rooms.add(player.current_room.id)

    visited[prev_room][current_direction] = player.current_room.id

    if player.current_room.id not in visited:
        visited[player.current_room.id] = {}
        visited[player.current_room.id][opposite(current_direction)] = prev_room

    current_direction = None
    
    unexplored_exits = 0
    for direction in player.current_room.get_exits():
        if direction not in visited[player.current_room.id]:
            current_direction = direction
            visited[player.current_room.id][direction] = "?"
            unexplored_exits += 1

    if unexplored_exits == 0:

        queue = Queue()
        explored = set()

        queue.enqueue(player.current_room.get_exits()[0])

        while queue.size() > 0 and current_direction == None:
            path = queue.dequeue()
            new_direction = path[-1]
            player.travel(new_direction)
            traversal_path.append(new_direction)
            if player.current_room.id not in explored:
                explored.add(player.current_room.id)

                for door in player.current_room.get_exits():
                    if visited[player.current_room.id][door] == "?":
                        current_direction = door
                    else:
                        queue.enqueue(new_direction)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room.id)

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
