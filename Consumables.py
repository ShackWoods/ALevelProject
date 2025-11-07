###IMPORTS###
from Sprite import Sprite
import pygame

#A class used to store a consumable entity in the game
class Consumable(Sprite):                                                       #Consumable is a subclass of the Sprite class
    def __init__(self, position: tuple, image, player):
        super().__init__(position, image)                                       #Instantiate the superclass (see Sprite for details)
        self.player = player
        self.collider = pygame.Rect(self.position, self.size)                   #Create a collider for the consumable

    #Function to test if the player has touched the consumable
    def touch_check(self) -> bool:
        player_collider = pygame.Rect(self.player.position, self.player.size)   #Create the player collider
        if(not self.collider.colliderect(player_collider)): return False        #Test for collision

        self.use()                                                              #Perform use if collided
        return True                                                             #Then flag for deletion

#A class used to store the method for an upgrade consumable
class Upgrade(Consumable):                                                      #Upgrade is a subclass of the Consumable class
    def __init__(self, position: tuple, image, player, upgrade: str):
        super().__init__(position, image, player)                               #Instantiate the superclass
        self.upgrade = upgrade

    #A function to "use" the consumable
    def use(self):
        if(self.player.upgrade == "Run"):                                       #If the player has the run upgrade
            self.player.max_speed //= 2                                         #half the player's speed
        if(self.upgrade == "Run"):                                              #If this is a run upgrade
            self.player.max_speed *= 2                                          #Double the player's speed
            
        self.player.upgrade = self.upgrade                                      #Then just set the upgrade variable

#A class used to store the method for a healing consumable
class Heal(Consumable):                                                         #Heal is a subclass of the Consumable class
    def __init__(self, position: tuple, image, player, amount: str):
        super().__init__(position, image, player)                               #Instantiate the superclass
        self.amount = -amount                                                   #Healing is just reverse damage

    #A function to "use" the consumable
    def use(self):
        self.player.damaged(self.amount, piercing = True)                       #Healing can happen if the player is invulnerable
