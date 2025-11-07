###IMPORTS###
import pygame

#An object which acts as a container of Entry objects
class Listbox:
    def __init__(self, position: tuple, entry_list: tuple, scrollbar):
        #Reposition all the entries
        self.position = list(position)                                      #The listbox can change position, so make sure it is mutable
        self.entries = entry_list
        total_height = 0
        self.entry_height = entry_list[0].image.get_height()                #Determine the height of an entry
        for entry in entry_list:                                            #Then for each entry
            entry.position = [0, total_height]                              #Reposition to be relative to the listbox
            total_height += self.entry_height                               #then update the current height of the listbox
            
        #Draw onto one image
        this_width = entry_list[0].image.get_width()                        #Determine the width of an entry
        self.image = pygame.Surface((this_width, total_height))             #Generate a big background
        for entry in entry_list:                                            #Then draw all the entries onto it
            entry.draw(self.image)
        
        self.shift = 0
        self.shift_bound = len(self.entries)-3                              #Can scroll up to number of entries - 3 time
        surface_height = self.entry_height * 3
        self.to_draw = pygame.Surface((this_width, surface_height))         #Generate a new image which is actually to be drawn
        self.to_draw.fill((50,50,50))                                       #Fill with a grey background
        self.shift_and_render(0)                                            #Perform the function to put it together

        self.scrollbar = scrollbar
        if(scrollbar is not None): self.scrollbar.make_relative(self)       #If a scrollbar is present, move it next to the listbox

    #A function which shifts the listbox up and down, and then renders the new image
    def shift_and_render(self, shift_amount: int):
        self.shift += shift_amount
        self.shift = min(self.shift, self.shift_bound)                      #Keep in bounds
        self.shift = max(self.shift, 0)

        self.to_draw.blit(self.image, (0, -self.entry_height * self.shift)) #Draw the active section of the big image onto the little image

        for x, entry in enumerate(self.entries):                            #Then active/deactivate the entries
            if(x < self.shift): entry.is_active = False                     #to make sure only displayed entries are active
            elif(x > self.shift + 2): entry.is_active = False
            else: entry.is_active = True

    #A function to draw the listbox onto a surface
    def draw(self, surface):
        surface.blit(self.to_draw, self.position)                           #Draw the active listbox (little image)
        if(self.scrollbar is not None): self.scrollbar.draw(surface)        #Draw the scrollbar if it exists

    #A function to perform the clicked check for each of the contained objects
    def clicked(self, mouse_down: bool, mouse_position):
        '''
        The "active" listbox moves, whereas the scrollbar remains the same
        -Thus different mouse position lists are necessary
        '''
        effective_top = (self.position[1] - self.entry_height * self.shift) #Determine where the top of the active listbox is
        mpA = [mouse_position[0] - self.position[0],                        #Make the mouse position relative to the active listbox
              mouse_position[1] - effective_top]                            #-for entries
        mpB = [mouse_position[0] - self.position[0],                        #Make the mouse position relative to the listbox
              mouse_position[1] - self.position[1]]                         #-for the scrollbar

        for entry in self.entries:                                          #Then for each ACTIVE entry, perform the clicked check
            if(entry.is_active): entry.clicked(mouse_down, mpA)
        if(self.scrollbar is not None):
            self.scrollbar.clicked(mouse_down, mpB)                         #Perform the scrollbar clicked check if it exists
