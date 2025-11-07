###IMPORTS###
from Sprite import Sprite
from Common_Functions import click_in_bounds

#An object which is used to scroll a listbox
class Scrollbar(Sprite):                                                                    #Scrollbar is a subclass of Sprite
    def __init__(self, position: tuple, image):
        super().__init__(position, image)                                                   #Instantiate the superclass (see Sprite for details)
        self.click_position = [0,0]
        self.owner = None
        self.active = False

    #A function to reposition the scrollbar next to a listbox
    def make_relative(self, new_owner):
        relative_x = new_owner.position[0] + new_owner.to_draw.get_width()                  #Scrollbar goes on the right side of the listbox
        self.position = [relative_x, new_owner.position[1]]                                 #Set the position relative to the listbox
        self.click_position = [new_owner.to_draw.get_width(), 0]

        self.owner = new_owner

    #Validate if a click starts and ends within the button
    def clicked(self, mouse_down: bool, mouse_position):
        bounds = (self.click_position[0], self.click_position[0] + self.size[0],            #The bounds of the scrollbar
                  self.click_position[1], self.click_position[1] + self.size[1])
        if(not click_in_bounds(mouse_position, bounds)):                                    #If not in bounds, unlatch and end
            self.active = False
            return
        
        if(self.active and not mouse_down):                                                 #If latched and releasing the mouse
            if(mouse_position[1] < 14): self.owner.shift_and_render(-1)                     #Shift 1 up if the top was clicked
            elif(mouse_position[1] > 178): self.owner.shift_and_render(1)                   #Shift 1 down if the bottom was clicked
            else:
                jump_to = ((mouse_position[1] - 14) * (self.owner.shift_bound + 1)) // 164  #Else determine what percentage of the
                                                                                            #scrollbar the click was
                to_shift = jump_to - self.owner.shift                                       #Then jump that percentage of the way into the listbox
                self.owner.shift_and_render(to_shift)
        if(mouse_down): self.active = True                                                  #Set the latch
