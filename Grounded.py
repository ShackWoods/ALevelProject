###IMPORTS###
from Combatant import Combatant
import pygame

#A class which walks left to right
class Grounded(Combatant):                                                                      #Grounded is a subclass of Combatant
    def __init__(self, position: tuple, image, start_health: int, weapon_info: tuple,
                 team: bool, has_hitbox: bool, max_speed: int, edge: int):
        super().__init__(position, image, start_health, weapon_info, team, has_hitbox)          #Instantiate the superclass (see Combatant for details)

        self.is_sticky = False
        self.facing = "right"
        self.speed = 0
        self.max_speed = max_speed

        self.jump_count = 0                                                                     #0 = grounded, 16 = jump maxxed
        self.fall_count = 0
        self.coyote_frames = 8                                                                  #8 = grounded
        self.double_jump = False
        self.jump_release = False

        self.dash_timer = 0

        self.screen_edge = edge - 32
        self.upgrade = None

    #A function which takes boolean inputs and causes the object to move accordingly
    def controller(self, inputs: tuple, platform_list: tuple, collider_list: tuple):
        self.vertical_logic(inputs[0], platform_list, collider_list)
        self.position[1] = max(self.position[1], 0)                                             #The object can't go off screen

        if(inputs[1] and not inputs[2]):                                                        #Move horizontally if the left and right
            self.horizontal_logic("left", platform_list, collider_list)                         #inputs satisfy an XOR gate
        elif(inputs[2] and not inputs[1]):
            self.horizontal_logic("right", platform_list, collider_list)
        else: self.horizontal_acceleration("none")

        if(self.upgrade == "Dash"):                                                             #If the player has the dash upgrade
            if(inputs[3] and self.dash_timer <= 0):                                             #If a dash is desired and possible
                self.speed = self.max_speed                                                     #Max out speed
                self.dash_timer = 15                                                            #Prevent dashing again for 15 frames
                for x in range(24):                                                             #Try to move 3 tiles in the current direction
                    self.horizontal_movement(self.facing, platform_list, collider_list)
            else: self.dash_timer -= 1                                                          #Decrement the timer

    #A function to incrementally move the objects forward
    def jiggle(self, direction: str, x_shift: int, y_shift: int, distance_to_move: int,
               platform_list: tuple, collider_list: tuple) -> bool:
        '''
        Move a little bit
        Check for collisions
        If collided, perform that platform's touched function
        Repeat until fully moved or collided
        '''

        displacement = 0
        collided = False
        while displacement < distance_to_move:                                                  #While I still want to move
            displacement += 1
            self.move(x_shift,y_shift)                                                          #Move

            my_collider = pygame.Rect(self.position, self.size)                                 #Generate my collider
            collision_index = my_collider.collidelist(collider_list)                            #Check if I collide with any platforms
            if(collision_index >= 0):
                if(platform_list[collision_index].touched(self, direction)):                    #Check if the movement is blocked
                    collided = True                                                             #If so, undo move and stop moving further
                    self.move(-x_shift,-y_shift)
                    break                
        self.position[0] = min(self.position[0], self.screen_edge)                              #Keep myself on screen
        self.position[0] = max(self.position[0], 0)

        return collided                                                                         #Return whether a collision occured

    #Polymorphically used in the player class - Here it is just a fall
    def vertical_logic(self, _, platform_list: tuple, collider_list: tuple):
        try:
            if(self.grounded): return                                                           #Do nothing if on a platform
        except: pass
        
        self.fall_count += 1                                                                    #Else accelerate downwards
        speed = self.fall_count // 2
        self.grounded = self.jiggle("down", 0, 1, speed, platform_list, collider_list)          #Set the grounded flag when you land

    #A function to accelerate and move horizontally
    def horizontal_logic(self, direction: str, platform_list: tuple, collider_list: tuple):
        self.horizontal_acceleration(direction)
        self.horizontal_movement(self.facing, platform_list, collider_list)

    #A function to accelerate/decellerate horizontally
    def horizontal_acceleration(self, direction: str):
        if(self.facing == direction):                                                           #If moving in the previous direction
            self.speed = min(self.speed + 1, self.max_speed)                                    #Get faster (up to a terminal velocity
        else:
            self.speed -= 1                                                                     #Else get slower

        if(self.speed < 0):                                                                     #If speed is negative, turn around
            if(direction != "none"): self.facing = direction
            self.speed = 0

    #A function to move the object horizontally
    def horizontal_movement(self, direction: str, platform_list: tuple, collider_list: tuple):
        match direction:                                                                        #Determine the direction of movement
            case "right": shift = 1     
            case "left": shift = -1

        self.jiggle(direction, shift, 0, self.speed, platform_list, collider_list)              #Then call jiggle to move as far as possible
