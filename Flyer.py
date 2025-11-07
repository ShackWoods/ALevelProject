###imports###
from Combatant import Combatant
from Finite_State_Machine import Flyer_FSM
import AStar
import random

#An enemy which flies around the screen, targeting the player
class Flyer(Combatant):                                                         #The flyer is a subclass of the Combatant class
    def __init__(self, position: tuple, image, player_object):
        health, damage = self.mutations()                                       #Randomise the flyer's stats
        
        super().__init__(position, image, health, (damage,4,1), False, False)   #Instantiate the superclass (see Combatant for details)

        self.fsm = Flyer_FSM(self, player_object)                               #Instantiate a finite state machine for the flyer
        self.move_timer = 0
        self.target_position = [0,0]

    #A function to randomise the flyer's stats
    def mutations(self):
        health_roll = random.randint(0,3)                                       #Randomly choose a number from 0 to 3
        if(health_roll == 3): health = 2                                        #Good roll = double health
        else: health = 1                                                        #Else, normal health
        
        damage_roll = random.randint(0,3)                                       #Randomly choose a number from 0 to 3
        if(damage_roll == 3): damage = 2                                        #Good roll = double damage
        else: damage = 1                                                        #Else, normal damage
        return health, damage                                                   #Return the randomised stats

    #A function to choose an action based on the finite state machine
    def interpret_fsm(self, grid, graph):
        state = self.fsm.current_state
        if(state == "idle"): return                                             #Don't do anything if idle
        if(state != "moving"):                                                  #If there is not a path found
            next_indices = self.pathfind(grid, graph)                           #Find the next indices on the path
            self.target_position = [32 * index for index in next_indices]       #Convert to a position
            self.move_timer = 16                                                #Only pathfind after 16 frames
        self.move_timer -= 1                                                    #Reduce timer

        horiz_direction = self.target_position[0] - self.position[0]            #Determine where the target is horizontally
        if(horiz_direction == 0): x_shift = 0                                   #Then move accordingly
        elif(horiz_direction > 0): x_shift = 2
        else: x_shift = -2

        vert_direction = self.target_position[1] - self.position[1]             #Determine where the target is vertically
        if(vert_direction == 0): y_shift = 0                                    #Then move accordingly
        elif(vert_direction > 0): y_shift = 2
        else: y_shift = -2
        self.move(x_shift, y_shift)                                             #Then actually move

    #A function to find the closest position on the path to the player  
    def pathfind(self, grid, graph) -> tuple:
        my_indices = (self.position[0] // 32, self.position[1] // 32)           #Determine the indices of the flyer and the player
        player_indices = (self.fsm.target.position[0] // 32,
                          self.fsm.target.position[1] // 32)

        result = AStar.a_star(grid, my_indices, player_indices, *graph)         #Use the AStar algorithm to find the shortest path

        if(type(result) is str):                                                #If "Fail" was returned, don't move
            result = my_indices
        
        return result                                                           #Return the indices of the position to target
