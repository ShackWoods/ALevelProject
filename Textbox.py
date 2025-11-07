###IMPORTS###
from Sprite import Sprite
from Common_Functions import text_to_image, click_in_bounds
import pygame
###Premade lists of strings I need to limit what the player can enter
from string import ascii_lowercase as LOW                                           #A list of lowercase letters (a -> z)
from string import digits as DIG                                                    #A list of digits (0 -> 9)

#An object which allows the user to enter text based data into the program
class Textbox(Sprite):                                                              #Textbox is a subclass of Sprite
    def __init__(self, position: list, size: tuple, fg: tuple, active_bg: tuple,
                 inactive_bg: tuple, base_message: str, max_length: int):
        super().__init__(position, pygame.Surface(size))                            #Instantiate the superclass (see Sprite for details)
        self.base_message = base_message
        self.max_length = max_length
        self.current_message = ""
        self.font = pygame.font.SysFont("Arial", 54)                                #Load the Arial 54 font
        self.fg = fg
        self.active_bg = active_bg
        self.inactive_bg = inactive_bg

        self.active = False
        self.using = False

        self.generate_image()                                                       #Generate the initial image

        self.caps = False
        self.del_timer = 0
        self.valid_keys = tuple([char for char in LOW + DIG] + ["space"])           #The player can only enter letters, digits or spaces

    #Auxiliary function for the main loop to read the textbox
    def get_message(self) -> str:
        return self.current_message

    #Function which updates the image to reflect the current message and state of the textbox
    def generate_image(self):
        message = self.current_message
        if(message == ""): message = self.base_message                              #If empty, use the base message

        if(self.using):                                                             #Select a background cover depending on the current state
            bg = self.active_bg
        else:
            bg = self.inactive_bg
        
        text_image = text_to_image(self.font, message, True, self.fg, bg)           #Generate an image from the text and background
        left = (self.image.get_width() - text_image.get_width()) // 2               #Centralise the text to the box
        
        self.image.fill(bg)                                                         #Clear the current image and fill with background colour
        self.image.blit(text_image, (left, 0))                                      #Then draw the new text image

    #Function to modify the current message
    def make_change(self, to_add = "", adding = True):
        if(not adding):                                                             #If backspace
            curmsg = self.current_message
            self.current_message = curmsg[:len(curmsg)-1]                           #trim one character
        elif(to_add == "space"):                                                    #Else add space
            self.current_message += " "
        else:                                                                       #Or the relevant character
            self.current_message += to_add
        self.generate_image()                                                       #Then update the image

    #Function to activate/deactivate the textbox
    def change_focus(self, new_state):
        self.using = new_state                                                      #Change state
        self.generate_image()                                                       #Then update the image

    #Function to detect if a click started and ended in the textbox
    def clicked(self, mouse_down: bool, mouse_position):
        bounds = (self.position[0], self.position[0] + self.size[0],                #The bounds of the textbox
                  self.position[1], self.position[1] + self.size[1])
        if(not click_in_bounds(mouse_position, bounds)):                            #If not in bounds
            self.active = False                                                     #Unlatch
            self.change_focus(False)                                                #Deactivate
            return
        
        if(self.active and not mouse_down):                                         #If latched and releasing mouse
            self.change_focus(True)                                                 #Activate
            self.active = False                                                     #Unlatch
        if(mouse_down): self.active = True                                          #Else latch

    #Function to read the keyboard inputs and add to the message
    def listen(self, this_key: str):
        if(this_key == "caps lock"):                                                #If caps lock pressed
            self.caps = not self.caps                                               #just invert the state of the caps lock
            return
                                                                                    #This is here to let you hold backspace down
        keys = pygame.key.get_pressed()                                             #Get all the keys which are currently down
        deletable = self.current_message != "" and self.del_timer == 0              #Can only delete if there is message to delete
                                                                                    #and its been 5 frames
        if(keys[pygame.K_BACKSPACE] and deletable):                                 #If backspace down
            self.del_timer = 5                                                      #Start the timer
            self.make_change(adding = False)                                        #Then remove a character (using the function)
            return
        
        if(len(self.current_message) == self.max_length): return                    #Can't add to a full textbox
        if(this_key not in self.valid_keys): return                                 #Can't add an invalid character (see above)
        
        shift = keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]                      #Check if a shift key is down
        
        if(self.caps ^ shift):                                                      #Bitwise XOR of caps lock and shift
            to_add = this_key.upper()                                               #Upper case
        else:
            to_add = this_key                                                       #Lower case
            
        self.make_change(to_add = to_add)                                           #Then make the change
            
