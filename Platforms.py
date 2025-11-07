###IMPORTS###
from Sprite import Sprite
import pygame

#touched() in all cases returns whether a collision should block movement
#Other platform effects are covered in the main document

#The standard platform that just blocks movement
class Std_Platform(Sprite):                                         #All platforms are subclasses of the Sprite class
    def __init__(self, position: tuple, image):
        super().__init__(position, image)                           #Instantiate the superclass (see Sprite for details)

    def touched(self, *_) -> bool:                                  #*_ allows for a polymorphic touched function, ignoring all parameters
        return True                                                 #Always block

#The honey platform blocks VERTICAL movement
class Honey_Platform(Sprite):
    def __init__(self, position: tuple, image):
        super().__init__(position, image)                           #Instanatiate the superclass

    def touched(self, collider, direction_of_motion: str) -> bool:
        try: collider.is_sticky = True                              #Mark the object as sticky (if possible)
        except: pass
        return direction_of_motion in ["up","down"]                 #Only block vertical motion

#The spike platform blocks all movement and deals damage
class Spike_Platform(Sprite):
    def __init__(self, position: tuple, image):
        super().__init__(position, image)                           #Instantiate the superclass

    def touched(self, collider, _) -> bool:                         #Ignore the direction of motion
        collider.damaged(1)                                         #Deal 1 damage
        return True

#The oway blocks entry from one direction
class One_Way_Platform(Sprite):
    def __init__(self, position: tuple, image, direction: str):
        super().__init__(position, image)                           #Instantiate the superclass
        self.direction = direction                                  #Note: an up one_way has a down blocking direction
        match direction:                                            #Determine where the blocking edge is
            case "down":
                alt_position = position
                alt_size = (32, 1)
            case "up":
                alt_position = (position[0], position[1] + 31)
                alt_size = (32, 1)
            case "left":
                alt_position = (position[0] + 31, position[1])
                alt_size = (1, 32)
            case "right":
                alt_position = position
                alt_size = (1, 32)
        self.edge = pygame.Rect(alt_position, alt_size)             #Generate a collider for that edge

    def touched(self, collider, direction_of_motion: str) -> bool:
        if(self.direction != direction_of_motion): return False     #If not moving in the blocked direction, then allow motion

        position = collider.position
        match self.direction:                                       #Generate a collider for the relevant edge on the colliding object
            case "up":
                alt_position = position
                alt_size = (32, 1)
            case "down":
                alt_position = (position[0], position[1] + 31)
                alt_size = (32, 1)
            case "right":
                alt_position = (position[0] + 31, position[1])
                alt_size = (1, 32)
            case "left":
                alt_position = position
                alt_size = (1, 32)
        col_edge = pygame.Rect(alt_position, alt_size)              #Generate the collider
        
        return self.edge.colliderect(col_edge)                      #Only block if the colliding object is ENTERING the platform

#A special platform, which doesn't block motion, but flags if the level is completed
class Flag(Sprite):
    def __init__(self, position: tuple, image):
        super().__init__(position, image)                           #Instantiate the superclass
        self.complete = False

    def touched(self, collider, _) -> bool:
        if(collider.is_player_team): self.complete = True           #Only mark as complete if collided with the player
        return False                                                #DON'T BLOCK MOTION
