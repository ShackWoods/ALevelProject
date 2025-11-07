###IMPORTS###
from Sprite import Sprite
from Button import Button
from Common_Functions import text_to_image
import pygame

#Function to generate the UI for the Editor Palette Button Tooltip Screen
def generate_buttons_UI(change_screen) -> list:
    '''
    Elements:
    -Return Button
    -List of controls
    '''
    return_img = pygame.image.load('Images/return_button.png').convert()                                    #Load the return, save, play
    save_img = pygame.image.load('Images/save.png').convert()                                               #draw and erase button images
    play_img = pygame.image.load('Images/play.png').convert()
    draw_img = pygame.image.load('Images/Draw.png').convert()
    erase_img = pygame.image.load('Images/Erase.png').convert()

    draw_img = pygame.transform.scale(draw_img, (64, 64))                                                   #Resize the draw and erase
    erase_img = pygame.transform.scale(erase_img, (64, 64))                                                 #images to match return, etc
    
    btnReturn = Button((0,0), return_img, change_screen, "#LEVELS")                                         #Instantiate the return button

    save_display = Sprite((128,32), save_img)                                                               #Create a sprite for each of the
    play_display = Sprite((128,112), play_img)                                                              #other images
    draw_display = Sprite((128,192), draw_img)
    erase_display = Sprite((128,272), erase_img)
    button_displays = [save_display, play_display, draw_display, erase_display]                             #Then store in a list

    font = pygame.font.SysFont("Arial", 54)                                                                 #Load the Arial 54 font
    fg, bg = (255,255,255), (50,50,50)                                                                      #White foreground, Grey background
    save_msg_img = text_to_image(font, "Save the level", True, fg, bg)                                      #Generate an image for each string
    play_msg_img = text_to_image(font, "Play the level", True, fg, bg)                                      #which will be used to explain what
    draw_msg_img = text_to_image(font, "Set mode to 'draw'", True, fg, bg)                                  #the buttons do
    erase_msg_img = text_to_image(font, "Set mode to 'erase'", True, fg, bg)
    scroll_msg_img = text_to_image(font, "Use black arrows to scroll", True, (0, 0, 0), bg)
    palette_msg_img = text_to_image(font, "Use purple arrows to change palette", True, (152, 68, 152), bg)   

    save_msg = Sprite((224,32), save_msg_img)                                                               #Instantiate a sprite for each msg
    play_msg = Sprite((224,112), play_msg_img)
    draw_msg = Sprite((224,192), draw_msg_img)
    erase_msg = Sprite((224,272), erase_msg_img)
    scroll_msg = Sprite((131,352), scroll_msg_img)
    palette_msg = Sprite((26,432), palette_msg_img)
    msg_displays = [save_msg, play_msg, draw_msg, erase_msg, scroll_msg, palette_msg]                       #Then store in a list
    
    return [btnReturn] + button_displays + msg_displays                                                     #Return the UI elements

#Function to generate the UI for the Editor Palette Keybinds Tooltip Screen
def generate_keybinds_UI(change_screen) -> list:
    '''
    Elements:
    -Return Button
    -List of keybinds
    '''
    return_img = pygame.image.load('Images/return_button.png').convert()                                    #Load the return button image
    btnReturn = Button((0,0), return_img, change_screen, "#LEVELS")                                         #Instantiate the return button

    messages = ["H: Hide save and play buttons", "M: Change mode",                                          #A list of the messages to
                "E: Set mode to 'erase'", "D: Set mode to 'draw'",                                          #be displayed
                "1: Change palette to tiles", "2: Change palette to entities",
                "3: Change palette to consumables", "LEFT: Scroll left",
                "RIGHT: Scroll right"]
    msg_buttons = []
    font = pygame.font.SysFont("Arial", 32)                                                                 #Load the Arial 32 font
    fg, bg = (255,255,255), (50,50,50)                                                                      #White foreground, Grey background
    for k, msg in enumerate(messages):                                                                      #For each message
        msg_img = text_to_image(font, msg, True, fg, bg)                                                    #Generate an image of the message

        x = (768 - msg_img.get_width()) // 2                                                                #Determine its position
        y = 32 + 48 * k                                                                                     #horizontally centered
        new_msg = Sprite((x,y), msg_img)                                                                    #Instantiate a Sprite object
        msg_buttons.append(new_msg)                                                                         #Append to the list

    return [btnReturn] + msg_buttons                                                                        #Return the UI elements
