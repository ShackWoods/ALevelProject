###IMPORTS###
from Combatant import Combatant
import pygame
import random

#A class for an enemy which crawls around a platform
class Crawler(Combatant):                                                   #The crawler is a subclass of the Combatant
    def __init__(self, position: tuple, image, grid):
        #Auxiliary function to make sure the neighbouring tile is real
        def validate(indices, shifts, grid, walls):
            modded_indices = [indices[x] + shifts[x] for x in range(2)]     #Determine the position of the neighbour

            if(modded_indices[0] < 0): return False                         #Guard clauses to reject non existant tiles
            if(modded_indices[1] < 0): return False
            if(modded_indices[0] >= len(grid[0])): return False
            if(modded_indices[1] > 15): return False
            
            tile = grid[modded_indices[1]][modded_indices[0]]               #If the tile is real
            return tile in walls                                            #Only valid if the tile is a platform
            
        health, damage, attack_time = self.mutations()                      #Mutate the crawler to make it unique
        
        super().__init__(position, image, 2, (1,4,15), False, False)        #Instantiate the superclass (see Combatant for details)
        
        my_indices = (position[0]//32, position[1]//32)                     #Convert position to indicies
        walls = ["Floor", "Honey", "Spike", "Uway", "Dway", "Rway", "Lway"] #The solid objects
        self.direction = "up"
        options = 0
        if(validate(my_indices, (-1,0), grid, walls)):                      #For each direction, mark if the crawler could spawn there
            self.direction = "up"                                           #i.e. has something to stick to
            options += 1
        if(validate(my_indices, (1,0), grid, walls)):
            self.direction = "down"
            options += 1
        if(validate(my_indices, (0,-1), grid, walls)):
            self.direction = "right"
            options += 1
        if(validate(my_indices, (0,1), grid, walls)):
            self.direction = "left"
            options += 1
            
        if(options == 0 or options == 4): self.destroy_flag = True          #Destroy if there's nothing to stick to, or fully trapped
        self.set_sticking_point()                                           #Determine the sticking direction

    #A function to randomise the stats of the crawler
    def mutations(self):
        health = random.randint(2,4)                                        #Health is 2 -> 4
        
        attack_roll = random.randint(0,7)                                   #Choose a random number from 0 to 7
        damage, attack_time = 1, 15                                         #Basic stats
        if(attack_roll < 2):                                                #Low roll (<2)
            attack_time = 30                                                #slow attacker
        elif(attack_roll >= 4 and attack_roll < 6):                         #Above average roll (4, 5)
            if(attack_roll % 2 == 0): damage = 2                            #either give a damage boost
            else: attack_time = 10                                          #or attack faster
        elif(attack_roll >= 6):                                             #Exceptional roll (6, 7)
            damage = 2                                                      #High damage and fast attacker
            attack_time = 10

        speed_roll = random.randint(0,3)                                    #Choose another random number from 0 to 3
        if(speed_roll == 0): self.speed = 1                                 #Bad roll = half speed
        elif(speed_roll == 3): self.speed = 4                               #Good roll = double speed
        else: self.speed = 2                                                #Average roll = normal speed

        return health, damage, attack_time                                  #Return the randomised stats

    #A function to determine the "sticking point" of the crawler
    def set_sticking_point(self):
        match self.direction:                                               #The sticking point is 90 degrees clockwise from the direction of motion
            case "up": self.sticking_point = "left"
            case "left": self.sticking_point = "down"
            case "down": self.sticking_point = "right"
            case "right": self.sticking_point = "up"

    #A function to rotate the crawler's direction by 90 degrees
    def rotate(self, clockwise: str):
        salted_direction = self.direction + clockwise                       #Clockwise and anticlockwise rotations are different
        match salted_direction:                                             #Just rotate 90 degrees in the indicated direction
            case "upc": self.direction = "right"
            case "upa": self.direction = "left"
            case "leftc": self.direction = "up"
            case "lefta": self.direction = "down"
            case "downc": self.direction = "left"
            case "downa": self.direction = "right"
            case "rightc": self.direction = "down"
            case "righta": self.direction = "up"

        self.set_sticking_point()                                           #Then update the sticking point

   #A function to determine if there is a platform in the indicated direction
    def shudder(self, shudder_direction: str, collider_list) -> bool:
        modded_position = [self.position[0], self.position[1]]              #Create a copy opf the current position to not have to undo a shift

        match shudder_direction:                                            #Shift the position in the indicated direction
            case "up": modded_position[1] -= self.speed
            case "down": modded_position[1] += self.speed
            case "left": modded_position[0] -= self.speed
            case "right": modded_position[0] += self.speed
        
        my_collider = pygame.Rect(modded_position, self.size)               #Generate a collider of where the crawler would be if it moved this way

        return my_collider.collidelist(collider_list) != -1                 #Return True if there is something in the way

    #The main function to determine what the crawler should do
    def logic(self, collider_list):
        if(self.shudder(self.direction, collider_list)):                    #If the next tile is blocked
            self.rotate("c")                                                #rotate clockwise
            return

        self.controller()                                                   #Move

        if(not self.shudder(self.sticking_point, collider_list)):           #If the crawler is no longer connected to a platform
            self.rotate("a")                                                #rotate anticlockwise

    #A function to logically move the crawler
    def controller(self):
        x_shift = y_shift = 0

        match self.direction:                                               #Determine what movement is necessary
            case "up": y_shift = -self.speed
            case "down": y_shift = self.speed
            case "left": x_shift = -self.speed
            case "right": x_shift = self.speed

        self.move(x_shift, y_shift)                                         #Then move
