###IMPORTS###
from Sprite import Sprite
from Common_Functions import click_in_bounds

#An object which runs a function when clicked
class Button(Sprite):                                                   #Button is a subclass of Sprite
    def __init__(self, position: tuple, image, action, *args):          #*args collates all final arguments into a list
        super().__init__(position, image)                               #Instantiate the superclass (see Sprite for details)
        self.action = action                                            #The function and parameters to be ran when clicked
        self.args = args
        self.active = False                                             #A variable acting as the latch

    #Validate if a click starts and ends within the button
    def clicked(self, mouse_down: bool, mouse_position):
        bounds = (self.position[0], self.position[0] + self.size[0],    #The button's bounds
                  self.position[1], self.position[1] + self.size[1])
        if(not click_in_bounds(mouse_position, bounds)):                #If not clicking the button
            self.active = False                                         #Unlatch and end
            return
        
        if(self.active and not mouse_down):                             #If latched AND releasing the mouse
            self.action(self.args)                                      #Run the function
            self.active = False                                         #Unlatch
        if(mouse_down): self.active = True                              #If pressing down, latch
