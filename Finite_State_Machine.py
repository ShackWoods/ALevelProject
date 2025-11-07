###IMPORTS###
from Common_Functions import pythagorus

#THESE CLASSES JUST TELL THE ENEMY WHAT THEY SHOULD BE DOING GENERALLY, NOT HOW TO DO IT

#A class storing the finite state machine for a walker enemy
class Walker_FSM:
    def __init__(self, owner, target):
        self.current_state = "idle"
        self.owner = owner
        self.target = target

    #See Finite State Machine Transition Diagram
    #Function to determine (and perform) if a state change is necessary
    def change_state(self):
        match self.current_state:
            case "idle":                                                                                #The do nothing state
                if(self.owner.on_screen):                                                               #Move when visible
                    self.current_state = "moving"

            case "moving":                                                                              #The just move state
                if(pythagorus(self.owner.position, self.target.position) <= self.owner.weapon_range):   #Attack when you can hit
                   self.current_state = "attacking"

                elif(not self.owner.on_screen):                                                         #Stay still when you're off screen
                    self.current_state = "idle"

            case "attacking":                                                                           #The attack the player state
                if(pythagorus(self.owner.position, self.target.position) > self.owner.weapon_range):    #Move when you can't hit
                   self.current_state = "moving"



#A class storing the finite state machine for a flyer enemy
class Flyer_FSM:
    def __init__(self, owner, target):
        self.current_state = "idle"
        self.owner = owner
        self.target = target

    #See Finite State Machine Transition Diagram
    def change_state(self):
        match self.current_state:
            case "idle":                                                                                #The do nothing state
                if(self.owner.on_screen):                                                               #If visible, "turn on"
                    self.current_state = "active"

            case "active":                                                                              #The pathfinding state
                if(not self.owner.on_screen):                                                           #If off screen, deactivate
                    self.current_state = "idle"

                elif(self.owner.move_timer > 0):                                                        #If path found, don't waste
                    self.current_state = "moving"                                                       #resources pathfinding

            case "moving":                                                                              #The path found, just move state
                if(self.owner.move_timer == 0):                                                         #If destination has been reached
                    self.current_state = "active"                                                       #pathfind again
        
