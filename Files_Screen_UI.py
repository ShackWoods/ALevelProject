###IMPORTS###
from Button import Button
from Textbox import Textbox
from Common_Functions import text_to_image
import pygame

#Function to generate the UI for the file select screen
def generate_UI(change_screen) -> list:
    '''
    Elements:
    -Return Button
    -List of save file buttons
    -Delete Button
    '''
    return_img = pygame.image.load('Images/return_button.png').convert()        #Load the return, heart, and health bar images
    heart_img = pygame.image.load('Images/heart.png').convert_alpha()
    bar_img = pygame.image.load('Images/health.png').convert()
    
    btnReturn = Button((0,0), return_img, change_screen, "#HOME")               #Instantiate the return button

    font = pygame.font.SysFont("Arial", 54)                                     #Load the Arial 54 font
    fg, bg = (0,0,0), (0,160,255)                                               #Black Foreground, Blue Background
    saves = open("save_data.txt", "r").read().split("\n")                       #Load the save data file
    save_btn_list = [None] * 3
    save_found = False
    for x, save in enumerate(saves):                                            #For each save file
        position = (34, 152 + 80 * x)                                           #Determine its position
        
        parts = save.split(", ")                                                #Separate the parts of the save file

        save_img = pygame.Surface((700,64))                                     #Generate the background for the button
        save_img.fill(bg)

        if(parts[3] == "-1"):                                                   #If the save is empty
            txt_img = text_to_image(font, "NEW SAVE", True, fg, bg)             #Generate an image to show that
            save_img.blit(txt_img, (234,0))
            newBtn = Button(position, save_img, change_screen, "#NEW GAME",x)   #Instantiate a button of for the new save
        else:
            save_found = True
            
            name_img = text_to_image(font, parts[0], True, fg, bg)              #Generate an image to show the save file's information
            lives_img = text_to_image(font, parts[1], True, fg, bg)
            health_img = text_to_image(font, parts[2], True, fg, bg)
            level_img = text_to_image(font, parts[3], True, fg, bg)
            
            save_img.blit(name_img, (16,0))                                     #Assemble it all into one image
            save_img.blit(heart_img, (400,0))
            save_img.blit(lives_img, (464,0))
            save_img.blit(bar_img, (528,0))
            save_img.blit(health_img, (536, 0))
            save_img.blit(level_img, (632,0))
            newBtn = Button(position, save_img, change_screen, "#GAME",x)       #Instantiate a button for that save
        save_btn_list[x] = newBtn                                               #Add to save button list

    controls_img = text_to_image(font, "Controls", True, fg, bg)                #Generate an image for the control tooltip button
    btnControls = Button((301,0), controls_img, change_screen, "#CONTROLS")     #Instantiate the control tooltip button

    if(save_found):                                                             #Only generate if a save exists to be deleted
        delete_img = text_to_image(font, "DELETE", True, fg, (255, 0, 0))       #Generate an image to go to the delete form
        btnDelete = [Button((594,0), delete_img, change_screen, "#DELETE")]     #Instantiate the send to delete button
    else:
        btnDelete = []
    
    nameEntry = Textbox((34,420),(700,64), fg, bg, (0,100,160), "New Name", 16) #Instantiate a textbox to enter a new username
        
    return [nameEntry, btnReturn, btnControls] + btnDelete + [*save_btn_list]   #Return the UI elements
