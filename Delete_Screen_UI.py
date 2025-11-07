###IMPORTS###
from Button import Button
from Textbox import Textbox
from Common_Functions import text_to_image
import pygame
###Premade lists and functions I need for the captcha###
from string import ascii_lowercase as LOW                                   #A list of lowercase characters (a -> z)
from string import ascii_uppercase as UP                                    #A list of uppercase characters (A -> Z)
from string import digits as DIG                                            #A list of digits (0 -> 9)
from random import choices                                                  #A function which generates a random string

#Function to generate the UI for the file delete screen
def generate_UI(change_screen, delete_save) -> list:
    '''
    Elements:
    -Return Button
    -List of save file buttons
    '''
    return_img = pygame.image.load('Images/return_button.png').convert()    #Load the return, heart, and healthbar images
    heart_img = pygame.image.load('Images/heart.png').convert_alpha()
    bar_img = pygame.image.load('Images/health.png').convert()
    
    btnReturn = Button((0,0), return_img, change_screen, "#FILES")          #Instantiate the return button

    font = pygame.font.SysFont("Arial", 54)                                 #Load the Arial 54 font
    fg, bg = (255,255,255), (0,0,0)                                         #White foreground, Black background
    saves = open("save_data.txt", "r").read().split("\n")                   #Load and read the save data file
    save_btn_list = [None] * 3                                              #Create an empty list for the save file buttons
    for x, save in enumerate(saves):                                        #For each save file:
        position = (34, 152 + 120 * x)                                      #Produce its position
        
        parts = save.split(", ")                                            #Separate the parts of a given save
        if(parts[3] == "-1"): continue                                      #If no save exists, then what would you delete?

        save_img = pygame.Surface((700,64))                                 #Create a background image for the button
        save_img.fill(bg)

        name_img = text_to_image(font, parts[0], True, fg, bg)              #Create an image for the username, lives
        lives_img = text_to_image(font, parts[1], True, fg, bg)             #health, and current level
        health_img = text_to_image(font, parts[2], True, fg, bg)
        level_img = text_to_image(font, parts[3], True, fg, bg)
            
        save_img.blit(name_img, (16,0))                                     #Draw each image onto the background image
        save_img.blit(heart_img, (400,0))
        save_img.blit(lives_img, (464,0))
        save_img.blit(bar_img, (528,0))
        save_img.blit(health_img, (536, 0))
        save_img.blit(level_img, (632,0))
        newBtn = Button(position, save_img, delete_save, x)                 #Instantiate a button for that save
        save_btn_list[x] = newBtn                                           #Add to list

    save_btn_list = list(filter((lambda x: x is not None), save_btn_list))  #Remove all "None" occurences in the list

    captcha = "".join(choices(LOW + UP + DIG, k = 5))                       #Generate a captcha
    nameEntry = Textbox((568,0),(200,64), fg, (160,0,0), bg, captcha, 5)    #Instantiate a textbox for the captcha
        
    return [nameEntry, btnReturn, *save_btn_list]                           #Return the list of elements
