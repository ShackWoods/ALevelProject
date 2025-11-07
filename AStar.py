###IMPORTS###
import heapq
from math import inf
from Common_Functions import pythagorus

#A class to store the information about the node
#Just a data container
class Node:
    def __init__(self, x, y):
        self.parent_x = 0
        self.parent_y = 0
        self.f = inf
        self.g = inf
        self.h = 0

#Determine if a point is in the grid
def is_in_grid(x, y, ROWS, COLS) -> bool:
    return (x >= 0) and (x < COLS) and (y >= 0) and (y < ROWS)

#Determine if you can move along the given vector in the given tile
def is_movable(tile, vector) -> bool:                                                   #Guard clauses to reject invalid moves
    if(tile in ["Floor","Spike"]): return False                                         #No moving in solid objects
    if(tile in ["Honey","Dway"] and vector[1] == -1): return False                      #No moving up in a down one-way
    if(tile in ["Honey","Uway"] and vector[1] == 1): return False                       #No moving down in an up one-way
    if(tile == "Rway" and vector[0] == -1): return False                                #No moving left in a right one-way
    if(tile == "Lway" and vector[0] == 1): return False                                 #No moving right in a left one-way
    return True                                                                         #Not bad -> Good :D

#Determine if you can move from (x,y) to (new_x,new_y)
def is_reachable(x, y, new_x, new_y, vector, grid) -> bool:
    curTile = grid[y][x]
    newTile = grid[new_y][new_x]

    if(not is_movable(newTile, vector)): return False                                   #Do either of the tiles
    if(not is_movable(curTile, vector)): return False                                   #reject the movement?

    if(abs(vector[0]) + abs(vector[1]) == 1): return True                               #Orthogonal movement is valid at this stage

    horizTile = grid[y][new_x]                                                          #A diagonal motion is a vertical and horizontal
    vertTile = grid[new_y][x]                                                           #motion, so test if it is valid for both
    return is_movable(horizTile, vector) and is_movable(vertTile, vector)

#Determine if the position is the destination
def is_destination(x, y, dest) -> bool:
    return x == dest[0] and y == dest[1]

#Calculates the h_value for a given positoin
def calculate_h_value(x, y, dest) -> int:
    return pythagorus((x,y), dest, scalar = 10)

#Trace the path from the start node to destination, returning the next node on the path
def trace_path(nodes, dest) -> tuple:
    path = []
    x = dest[0]
    y = dest[1]

    while not (nodes[y][x].parent_x == x and nodes[y][x].parent_y == y):                #Just follow the pointers in the nodes
        path.append((x, y))
        temp_x = nodes[y][x].parent_x
        temp_y = nodes[y][x].parent_y
        x = temp_x
        y = temp_y

    return path[-1]                                                                     #The path is traced from destination to start

#A shortest-path pathfinding algorithm from a source (src) node to a destination (dest) node
def a_star(grid, src, dest, ROWS, COLS):
    if(src == dest):                                                                    #Don't move if already at the end
        return src

    closed_list = [[False for x in range(COLS)] for y in range(ROWS)]                   #Initialise the closed list and graph (nodes)
    nodes = [[Node(x,y) for x in range(COLS)] for y in range(ROWS)]

    x = src[0]                                                                          #(Initialise) and point the source node at itself
    y = src[1]
    source_node = nodes[y][x]
    source_node.f = source_node.g = source_node.h = 0
    source_node.parent_x = x
    source_node.parent_y = y

    open_list = []
    heapq.heappush(open_list, (0.0, x, y))

    vectors = [(0, 1), (0, -1), (1, 0), (-1, 0),                                        #Just a list of vectors to adjacent nodes
               (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while len(open_list) > 0:                                                           #Loop until all options considered
        p = heapq.heappop(open_list)                                                    #Select the closest option (smallest f)

        x = p[1]
        y = p[2]
        closed_list[y][x] = True                                                        #Mark as visited (the shortest path here has been found)

        for vector in vectors:                                                          #Consider each neighbouring node
            new_x = x + vector[0]
            new_y = y + vector[1]

            if(not is_in_grid(new_x, new_y, ROWS, COLS)): continue                      #Ignore if not real
            if(not is_reachable(x, y, new_x, new_y, vector, grid)): continue            #Ignore if not reachable
            if(closed_list[new_y][new_x]): continue                                     #Ignore if visited

            neighbour = nodes[new_y][new_x]

            if(is_destination(new_x, new_y, dest)):                                     #If neighbour is destination then we're done
                neighbour.parent_x = x                                                  #This only works as our nodes lie on a grid
                neighbour.parent_y = y
                trace_path(nodes, dest)
                return trace_path(nodes, dest)
            else:
                g_new = nodes[y][x].g + pythagorus((x, y), (new_x, new_y), scalar = 10) #Calculate updated values for f, g, and h
                if(neighbour.f == inf):                                                 #Only update h if this is the first visit
                    h_new = calculate_h_value(new_x, new_y, dest)
                else: h_new = neighbour.h
                f_new = g_new + h_new

                if(neighbour.f > f_new):                                                #If using this node is part of a shorter path to the neighbour
                    heapq.heappush(open_list, (f_new, new_x, new_y))                    #Add the neighbour to the open list
                    
                    neighbour.f = f_new                                                 #Update the neighbour information
                    neighbour.g = g_new
                    neighbour.h = h_new
                    neighbour.parent_x = x
                    neighbour.parent_y = y

    return "Fail"                                                                       #Failsafe if destination could not be reached
