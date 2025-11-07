###IMPORTS###
from Sprite import Sprite
from Button import Button
from Common_Functions import text_to_image
import pygame

#Function to create the UI for the Control Screen
def generate_UI(change_screen) -> list:
    '''
    Elements:
    -Return Button
    -List of controls as images
    '''
    return_img = pygame.image.load('Images/return_button.png').convert()            #Load the return button image
    btnReturn = Button((0,0), return_img, change_screen, "#FILES")                  #Instantiate the return button

    font = pygame.font.SysFont("Arial", 54)                                         #Load the Arial 54 font
    fg, bg = (255,255,255), (50,50,50)                                              #White foreground, Grey background
    title_img = text_to_image(font, "CONTROLS", True, fg, bg)                       #Create images of the inputted text
    left_img = text_to_image(font, "Left or A to move left", True, fg, bg)
    right_img = text_to_image(font, "Right or D to move right", True, fg, bg)
    jump_img = text_to_image(font, "Up or W to jump", True, fg, bg)
    pause_img = text_to_image(font, "P to pause", True, fg, bg)
    attack_img = text_to_image(font, "Space to attack", True, fg, bg)

    title = Sprite((261,16), title_img)                                             #Instantiate a Sprite of each text
    left_tip = Sprite((181,96), left_img)
    right_tip = Sprite((149,176), right_img)
    jump_tip = Sprite((223,256), jump_img)
    pause_tip = Sprite((278,336), pause_img)
    attack_tip = Sprite((231,416), attack_img)

    return [btnReturn, title, left_tip, right_tip, jump_tip, pause_tip, attack_tip] #Return the generated objects
