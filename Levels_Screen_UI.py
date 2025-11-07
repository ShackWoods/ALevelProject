###IMPORTS###
from Sprite import Sprite
from Button import Button
from Entry import Entry
from Listbox import Listbox
from Scrollbar import Scrollbar
from Textbox import Textbox
from Common_Functions import text_to_image
import pygame
import glob

#Generic function to generate the label for an entry object
def generate_label(text: str, font, bg: tuple):
    label = pygame.Surface((620,64))                                                    #Generate a background
    label.fill(bg)                                                                      #Using the passed bg colour
    label.blit(text_to_image(font, text, True, (0,0,0), bg), (0,0))                     #Generate an image for the text and draw onto the bg
    return Sprite((0,0), label)                                                         #Instantiate and return a Sprite for the image

#Function to generate the Level Select Screen UI
def generate_UI(change_screen) -> list:
    '''
    Elements:
    -Return Button
    -Tooltip Buttons
    -List of all custom levels
    '''
    return_img = pygame.image.load('Images/return_button.png').convert()                #Load the return, play, and scroll images
    play_img = pygame.image.load('Images/play.png').convert()
    scroll_img = pygame.image.load('Images/scroll_bar.png').convert_alpha()

    font = pygame.font.SysFont("Arial", 54)                                             #Load the Arial 54 font

    controls_img = text_to_image(font, "Buttons", True, (255,255,255), (63,72,204))     #Generate an image for the buttons which load
    keybinds_img = text_to_image(font, "Keybinds", True, (255,255,255), (200,191,231))  #the tool tips screens
    btnControls = Button((308, 0), controls_img, change_screen, "#TIPS", "Buttons")     #Instantiate the two buttons
    btnKeybinds = Button((292, 62), keybinds_img, change_screen, "#TIPS", "Keybinds")
    
    bgA, bgB = (0,160,255), (0,255,160)                                                 #Blue background, Mint background
    levels = [level[14:len(level)-4] for level in glob.glob('Levels/Custom/*.csv')]     #Find all the custom level files
                                                                                        #then trim to just show the level name
                                                                                        #not the file path and file format
    entry_list = [None] * (len(levels) + 1)                                             #Initialise a list
    lbl_new_level = generate_label("NEW LEVEL", font, bgA)                              #Generate the label for the NEW LEVEL Entry
    btn_new_level = Button((0,0), play_img, change_screen, "#NEW LEVEL")                #Generate the button for the NEW LEVEL Entry
    entry_list[0] = Entry((0,0), lbl_new_level, btn_new_level, True)                    #Insert the entry at position 0
    for x, level in enumerate(levels):                                                  #For each level
        if(x % 2 == 0): this_bg = bgB                                                   #Choose an alternating background colour
        else: this_bg = bgA
        
        this_label = generate_label(level, font, this_bg)                               #Generate the label for the entry
        this_button = Button((0,0), play_img, change_screen, level)                     #Generate the button for the entry
        this_entry = Entry((0,0), this_label, this_button, True)                        #Instantiate the entry using the label and button
        entry_list[x+1] = this_entry                                                    #Add to the list

    btnReturn = Button((0,0), return_img, change_screen, "#HOME")                       #Instantiate the return button
    #Minimum of 3 custom levels to scroll
    if(len(entry_list) > 2): scroll = Scrollbar((0,0), scroll_img)                      #Only instantiate a scrollbar if scrolling is
    else: scroll = None                                                                 #necessary
    lstLevels = Listbox((34,152), entry_list, scroll)                                   #Then instantiate a listbox of the entries

    nameEntry = Textbox((34,420),(700,64), (0,0,0), bgA, (0,100,160), "New Name", 18)   #Instantiate a textbox for level name entry
        
    return [nameEntry, btnReturn, btnControls, btnKeybinds, lstLevels]                  #Return the list of elements
