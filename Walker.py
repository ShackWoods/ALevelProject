###IMPORTS###
import Grounded
from Finite_State_Machine import Walker_FSM
import random

#This class is for an enemy which walks left to right on a platform
class Walker(Grounded.Grounded):                                                        #Walker is a subclass of Grounded
    def __init__(self, position: tuple, image, player_object, edge: int):
        health, damage, attack_time, speed = self.mutations()                           #Randomise the stats

        weapon = (damage, 32, attack_time)                                              #Grouping weapon info just to make the next line shorter
        super().__init__(position, image, health, weapon, False, True, speed, edge)     #Instantiate the superclass (see Grounded for details)

        self.fsm = Walker_FSM(self, player_object)                                      #Instantiate an FSM

    #A function to randomise the stats of the class
    def mutations(self):
        health = random.randint(2,4)                                                    #Pick a random number from 2 -> 4
        
        weapon_roll = random.randint(0,7)                                               #Pick a random number from 0 -> 7
        damage, attack_time = 1, 15                                                     #The basic stats
        if(weapon_roll < 2):                                                            #On a low roll (0, 1), attack slower                           
            attack_time = 30
        elif(weapon_roll >= 4 and weapon_roll < 6):                                     #On a good roll (4, 5), do more damage or attack faster
            if(weapon_roll % 2 == 0): damage = 2
            else: attack_time = 10
        elif(weapon_roll >= 6):                                                         #On an exceptional roll (6, 7), do more damage and attack faster
            damage = 2
            attack_time = 10

        speed_roll = random.randint(0,3)                                                #Pick a random number from 0 -> 3
        if(speed_roll == 0): speed = 1                                                  #On a bad roll (0), move slowly
        elif(speed_roll == 3): speed = 4                                                #On a good roll (3), move quickly
        else: speed = 2                                                                 #Else move normal speed

        return health, damage, attack_time, speed

    #A function to determine how the Walker should move
    def logic(self, grid, platform_list, collider_list):
        move_inputs = self.interpret_fsm(grid)                                          #Reads the state of the FSM to determine how to move
        self.controller(move_inputs, platform_list, collider_list)                      #Then perform the move (method of the superclass)

    #A function to read/interpret the FSM
    def interpret_fsm(self, grid) -> tuple:
        state = self.fsm.current_state
        
        player_visible = self.is_player_visible(grid)                                   #Determine if the player is visible
        if(state == "attacking" and player_visible): return (False,False,False,False)   #Don't move if in combat with the player
        return [False] + self.determine_move(player_visible, grid) + [False]            #Else determine how to move

    #Check if the player is in-line with the walker and not behind a wall
    def is_player_visible(self, grid) -> bool:
        x_index = self.position[0] // 32                                                #Determine the grid position
        y_index = self.position[1] // 32

        player_position = self.fsm.target.position                                      #Detemrine the player's position
        player_indices = (player_position[0] // 32, player_position[1] // 32)           #And where that is on the grid
        if(player_indices[1] != y_index): return False                                  #Check if the two objects are in-line

        if(self.facing == "left"):                                                      #Determine:
            if(player_indices[0] > x_index): return False                               #If the player is even in this direction
            shift = -1                                                                  #How to traverse the grid
            bound = -1                                                                  #When to stop
            block_list = ["Spike","Floor","Rway"]                                       #And what counts as a wall
        else:
            x_index -= 1                                                                #Make sure we're considering the left side of the walker
            if(player_indices[0] < x_index): return False
            shift = 1
            bound = len(grid[0])
            block_list = ["Spike","Floor","Lway"]

        for this_x in range(x_index, bound, shift):                                     #Step across the grid in the determine direction
            if(grid[y_index][this_x] in block_list): return False                       #If you reach a wall, then the player is hiden
        return False                                                                    #The search failed otherwise

    #A function to determine how to move
    def determine_move(self, player_visible: bool, grid) -> list:
        y_index = self.position[1] // 32                                                #Find what row the walker is on

        match self.facing:
            case "left":                                                                #Determine:
                vector = -1                                                             #How to move
                x_index = ((self.position[0] - 2) // 32) + 1                            #Which side (left or right) to consider <- this case is left
                block_list = ["Spike","Floor","Rway"]                                   #What stops movement
                new_face = "right"                                                      #And how to turn around
            case "right":
                vector = 1
                x_index = (self.position[0] + 2) // 32
                block_list = ["Spike","Floor","Lway"]
                new_face = "left"

        state = "normal"
        next_x = x_index + vector                                                       #Determine the tiles in front
        unwalkable = ["","Uway","Spike"]
        if(next_x < 0 or next_x >= len(grid[0])): state = "turn"                        #Turn if you reach the screen edge
        elif(grid[y_index][next_x] in block_list): state = "turn"                       #Turn if there is something in the way
        elif(grid[y_index + 1][next_x] in unwalkable): state = "turn"                   #Turn if you reach a platform's edge

        moves = [False, False]
        if(state == "normal" or player_visible):                                        #Only turn if the state is turn and the player isn't visible
            moves[(vector + 1) // 2] = True                                             #Covert the vector to an index
        elif(state == "turn"):
            self.facing = new_face
        
        return moves                                                                    #Tell the logic method how to move
