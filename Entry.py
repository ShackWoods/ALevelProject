###IMPORTS###
import pygame

#An object which stores a label and a button, used as an entry of a listbox
class Entry:
    def __init__(self, position: list, label, button, is_active: bool):
        self.position = position                                        #Determine and set the dimensions of the object
        image_width = label.size[0] + button.size[0]
        image_height = max(label.size[1], button.size[1])
        self.image = pygame.Surface((image_width, image_height))        #Generate a background for the label and button
        
        label.position = [0,0]                                          #Reposition the label and button to be
        button.position = [label.size[0],0]                             #relative to the entry
        label.draw(self.image)                                          #Then draw onto the background
        button.draw(self.image)

        del label                                                       #Destroy the label to save memory
        self.button = button                                            #Keep track of the button
        self.is_active = is_active                                      #Stores whether the entry is currently ON the listbox

    #A function to draw the entry to the screen
    def draw(self, surface):
        surface.blit(self.image, self.position)

    #A function to check if the label's button was clicked
    def clicked(self, mouse_down: bool, mouse_position):
        relative_position = (mouse_position[0] - self.position[0],      #Reposition the click position to be relative
              mouse_position[1] - self.position[1])                     #to the entry (like the button is)
        self.button.clicked(mouse_down, relative_position)              #Then let the button perform the click checks
