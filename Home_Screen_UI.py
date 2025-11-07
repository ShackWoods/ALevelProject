###IMPORTS###
from Sprite import Sprite
from Button import Button
from Common_Functions import text_to_image
import pygame

#Function to generate the UI for the home screen
def generate_UI(change_screen) -> list:
    '''
    Elements:
    -Title
    -File Select Button
    -Level Select Button
    '''
    big_font = pygame.font.SysFont("Arial", 72)                             #Load the Arial 72 font for the title
    lil_font = pygame.font.SysFont("Arial", 48)                             #Load the Arial 48 font for the buttons

    title_img = big_font.render("GAME GAME", True, (255,255,255))           #Create an image for the title, and two buttons
    files_img = text_to_image(lil_font, "FILE SELECT", True, (101,254,95))
    levels_img = text_to_image(lil_font,"LEVEL EDITOR", True, (255,0,0))
    
    lblTitle = Sprite((200,50), title_img)                                  #Instantiate a Sprite for the title
    btnFiles = Button((265,200), files_img, change_screen, "#FILES")        #Instantiate the two buttons
    btnLevels = Button((250,290), levels_img, change_screen, "#LEVELS")

    return [lblTitle, btnFiles, btnLevels]                                  #Return the elements
