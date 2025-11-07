###IMPORTS###
import Grounded
import pygame

#This is the class to represent the player's character
class Player(Grounded.Grounded):                                                                #This is a subclass of Grounded
    def __init__(self, position: tuple, image, start_lives: int, start_health: int, edge: int):
        super().__init__(position, image, start_health, (1,32,60), True, True, 4, edge)         #Instantiate the superclass (See Grounded for details)
        
        self.lives = start_lives

    #A function to determine how to move vertically each frame (overrides the superclass)
    def vertical_logic(self, jump_pressed: bool, platform_list: tuple, collider_list: tuple):
        '''
        Being sticky prevents vertical movement
        Jumping takes precendence over falling
        '''
        
        if(self.is_sticky):                                                                     #Check if you are on/under a honey tile
            self.coyote_frames = 0                                                              #Prevent coyote jumping out of honey
            honey_list = [pygame.Rect(plat.position, plat.size)                                 #Create a simplified list of just honey tiles
                          for plat in platform_list
                          if str(type(plat))[18:23] == "Honey"]
            modded_position = (self.position[0], self.position[1] - 1)                          #Make the player temporarily 2 pixels taller
            modded_size = (self.size[0], self.size[1] + 2)
            big_collider = pygame.Rect(modded_position, modded_size)                            #Create a collider for the modified player
            collision_index = big_collider.collidelist(honey_list)                              #Test if the player collides with a honey tile
            if(collision_index < 0): self.is_sticky = False                                     #If not, then unflag sticky
            return                                                                              #Always end vertical movement if you were sticky
        if(self.jump_conditions(jump_pressed, collider_list)):                                  #Check if you can/want to jump
            self.jump(platform_list, collider_list)                                             #-Jump if so
        else: self.fall(jump_pressed, platform_list, collider_list)                             #Else fall

    #A function to check if the player can jump and wants to jump
    def jump_conditions(self, jump_pressed: bool, collider_list: tuple) -> bool:
        '''
        Double Jump Conditions:
        1 - Double jump available
        2 - First jump complete
        '''
        d_jump_condition = self.upgrade == "DJump" and not self.double_jump                     #Check if a double jump is an option
        first_jump_complete = self.jump_release and self.jump_count == 16                       #Check that the first jump is done
        if(d_jump_condition and first_jump_complete):                                           #If both are the case
            if(jump_pressed):                                                                   #AND you want to jump
                self.jump_count = 0                                                             #Perform a double jump by resetting the jump_count
                self.double_jump = True                                                         #Then flag the double jump
                return True
            return False

        '''
        Wall Jump Conditions:
        1 - Touching a wall
        2 - First jump complete
        '''
        if(self.upgrade == "WJump" and first_jump_complete):                                    #Check if wall jumping is an option
            left_position = [self.position[0] - 1, self.position[1]]                            #Determine the pixels directly to the left
            right_position = [self.position[0] + 32, self.position[1]]                          #And right of the player
            modded_size = [1, self.size[1]]
            left_collider = pygame.Rect(left_position, modded_size)                             #Create a collider for each
            right_collider = pygame.Rect(right_position, modded_size)
            left_collision = left_collider.collidelist(collider_list) >= 0                      #Test for a collision on each (i.e. there is a wall)
            right_collision = right_collider.collidelist(collider_list) >= 0

            condition = left_collision or right_collision
            if(condition and jump_pressed):                                                     #If there is a wall and you want to jump
                self.jump_count = 4                                                             #A wall jump is slightly weaker
                self.fall_count = 0

                                                                                                #XOR the collision conditions to:
                if(left_collision and not right_collision):                                     #Bounce right off of a left wall
                    self.facing = "right"
                    self.speed = 4
                elif(right_collision and not left_collision):                                   #Bounce left off of a right wall
                    self.facing = "left"
                    self.speed = 4
                                                                                                #If XOR fails then we are between two walls
                return True
            
                                                                                                #A jump must last at least 8 frames
        try_jumping = jump_pressed or (self.jump_count > 0 and self.jump_count < 8)             #Check if the player pressed jump or a jump is in progress
                                                                                                #Then jump if you want to AND coyote frames remain
        return try_jumping and self.coyote_frames > 0 and self.jump_count < 16                  #AND you've not reached the top of a jump

    #A function to actually perform a jump
    def jump(self, platform_list: tuple, collider_list: tuple):
        self.jump_release = False                                                               #A flag to say that the jump key was/wasn't released
        
        self.coyote_frames = 1                                                                  #Prevent double_jumping by quickly tapping
        collided = self.jiggle("up", 0, -1, 8, platform_list, collider_list)                    #Then jiggle upwards into place
        
        if(collided): self.jump_count = 16                                                      #Colliding is the same as reaching the top of a jump
        else: self.jump_count += 1                                                              #Else just increment the timer

    #A function to accelerate the player downwards
    def fall(self, jump_pressed: bool, platform_list: tuple, collider_list):
        self.fall_count += 1                                                                    #Just a timer
        speed = self.fall_count // 2                                                            #V = U + AT => U = 0, A = 1/2 => V = T/2 (Kinematics)
        grounded = self.jiggle("down", 0, 1, speed, platform_list, collider_list)               #Jiggle downwards into place

        if(not jump_pressed):                                                                   #Check if the jump key was released
            self.jump_release = True
        if(grounded):
            if(self.jump_release):                                                              #Only allow jump when the jump key is released
                self.jump_count = 0
                self.jump_release = False
            self.fall_count = 0                                                                 #Reset the other variables
            self.coyote_frames = 8
            self.double_jump = False
        else:
            self.coyote_frames -= 1                                                             #Reduce coyote_frames
            if(self.coyote_frames <= 0): self.jump_count = 16                                   #If coyote jump is no longer an option then max out jump

    #A function to decrement the life counter rather than delete the player (override the superclass)
    def dead(self):
        if(self.health >= 0): self.lives -= 1
        return True
