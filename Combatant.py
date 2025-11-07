###IMPORTS###
from Sprite import Sprite
import pygame

#A class used to represent any damageable object (player and enemies)
class Combatant(Sprite):                                                                #Combatant is a subclass of the Sprite class
    def __init__(self, position: tuple, image, start_health: int,
                 weapon_info: tuple, team: bool, draw_hitbox: bool):
        super().__init__(position, image)                                               #Instantiate the superclass (see Sprite for details)
        self.health = start_health
        
        self.weapon_damage = weapon_info[0]
        self.weapon_range = weapon_info[1]
        self.weapon_duration = weapon_info[2]
        self.locked = 0
        self.invulnerable = 0

        self.is_player_team = team
        self.draw_hitbox = draw_hitbox
        self.upgrade = None                                                             #Only used for the player

    #A function to determine if the object is attacking
    def attack(self, packet_list, facing = False, first_call = True) -> list:
        '''
        Check if the attack is possible
        Create the hitbox
        Create a packet
        Start the lock timer
        '''
        if(self.locked > 0 or not self.on_screen): return packet_list                   #Can't attack if invisible, or attacked recently

        if(not facing):                                                                 #Flyers and Crawlers are their own hitbox
            hitbox = pygame.Rect(self.position, self.size)                              #Generate a collider for the object
        else:                                                                           #Player and Walkers use a "weapon"
            if(facing == "left"):                                                       #Determine what direction the object is attacking
                left = self.position[0] - self.weapon_range
            else:
                left = self.position[0] + self.size[0]
            hitbox_position = (left, self.position[1])                                  #Generate a collider for the weapon
            hitbox_size = (self.weapon_range, self.size[1])
            hitbox = pygame.Rect(hitbox_position, hitbox_size)

        packet = (hitbox, self)
        packet_list.append(packet)                                                      #Add to the current list of attacks

        if(self.upgrade == "DStrike" and first_call):                                   #If the player has double strike, and this is the first strike
            if(facing == "left"):                                                       #strike again in the opposite direction
                packet_list = self.attack(packet_list, "right", first_call = False)
            else: packet_list = self.attack(packet_list, "left", first_call = False)

        self.locked = self.weapon_duration                                              #Prevent spam attacking

        return packet_list                                                              #Return the list of attacks

    #A function to determine whether the attack killed the combatant
    def damaged(self, damage_amount: int, piercing = False) -> bool:
        if(self.invulnerable > 0 and not piercing): return False                        #If in an invulnerable state
        
        self.health -= damage_amount
        
        if(self.health <= 0):                                                           #If health <= 0, you die
            return self.dead()                                                          #A function is used specifically for the player
        
        self.invulnerable = 60                                                          #Mark the object as invulnerable for 60 frames
        return False                                                                    #Mark the object as alive

    def dead(self) -> bool:
        return True

    #LOGIC-FREE MOVEMENT - JUST REPOSITION
    def move(self, x_shift: int, y_shift: int):
        self.position[0] += x_shift
        self.position[1] += y_shift
