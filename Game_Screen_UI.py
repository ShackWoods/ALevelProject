###IMPORTS###
from Sprite import Sprite
from Button import Button
from Common_Functions import text_to_image
import pygame

#The game screen has an overlay for the health bar and timer
#Or can be paused to reveal a pause screen
class Game_UI:
    def __init__(self, game_control):
        self.game = game_control                                                            #The current object storing the game itself
        self.main_menu = game_control.main_menu                                             #The current object storing the menu
                                                                                            #-importantly, it stores the UI driver code
        self.common_imgs = {"heart": pygame.image.load('Images/heart.png').convert_alpha(), #A dictionary of the heart and health images                           
                            "health": pygame.image.load('Images/health.png').convert()}     #which are used in both the game and the
                                                                                            #pause screens
        self.main_UI = []                                                                   #Lists to store the UI generated
        self.pause_UI = []

    #Function to generate the UI overlay whilst the game is running
    def generate_main_ui(self):
        '''
        Elements:
        -Life count
        -Health bar
        -Timer
        '''
        life_UI = pygame.Surface((140,64))                                                  #Create a light grey background for
        life_UI.fill((150,150,150))                                                         #the life and health bar
        health_UI = pygame.Surface((70,64))
        health_UI.fill((150,150,150))
        
        lives = self.game.player.lives                                                      #Read the player's current life and health
        health = self.game.player.health
        raw_time = self.game.timer                                                          #Read the current time
        time_in_seconds = raw_time // 60                                                    #Then convert to seconds
        
        font = pygame.font.SysFont("Arial", 54)                                             #Load the Arial 54 font
        fg, bg = (0,0,0), (150,150,150)                                                     #Black foreground, Light Grey background
        life_img = text_to_image(font, str(lives), True, fg, bg)                            #Create an image for the life, health and time
        health_img = text_to_image(font, str(health), True, fg, bg)
        timer_img = text_to_image(font, str(time_in_seconds), True, fg, bg)

        life_UI.blit(self.common_imgs["heart"], (0,0))                                      #Draw the life symbol and life image
        life_UI.blit(life_img, (60,0))                                                      #Onto the life display image
        health_UI.blit(self.common_imgs["health"], (0,0))                                   #Do the same for the health display image
        health_UI.blit(health_img, (10,0))

        life_display = Sprite((0,0), life_UI)                                               #Instantiate a sprite for each image
        health_display = Sprite((140,0), health_UI)
        timer_x = 768 - timer_img.get_width()                                               #(The timer is on the right side)                                       
        timer_display = Sprite((timer_x,0), timer_img)
        self.main_UI = [life_display, health_display, timer_display]                        #Store to the main UI list

    #Function to generate the UI for te pause screen
    def generate_pause_ui(self):
        '''
        Elements:
        -Repositioned Life, Health, and Timer displays
        -Background
        -Return Button
        -Quit Button
        '''
        self.generate_main_ui()                                                             #All elements on the overlay above can be
        for element in self.main_UI:                                                        #repositioned for the pause screen
            element.position[0] += 200                                                      #The repositioning method
            element.position[1] += 120
        self.main_UI[2].position[0] -= 400                                                  #Pull the timer to the center of the screen

        background_img = pygame.Surface((500,400))                                          #Generate a background for the screen
        background_img.fill((30,30,30))                                                     #Dark grey fill

        font = pygame.font.SysFont("Arial", 66)                                             #Load the Arial 66 font
        fg = (0,0,0)                                                                        #Black foreground
        return_img = text_to_image(font, "RETURN", True, fg, (0,255,0))                     #Create the return button image (green bg)
        quit_img = text_to_image(font, "QUIT", True, fg, (255,0,0))                         #Create the quit button image (red background)
        
        background = Sprite((134,56), background_img)                                       #Instantiate the background as a Sprite                              
        returnBtn = Button((363,320), return_img, self.resolve_pause, True)                 #Instantiate the two buttons
        quitBtn = Button((180,320), quit_img, self.resolve_pause, False)
        
        self.pause_UI = [background, returnBtn, quitBtn]                                    #Store the UI in one place
        self.pause_UI += self.main_UI

    #Function to control what the return and quit buttons do
    def resolve_pause(self, return_to_game: bool):
        if(return_to_game[0]):                                                              #If returning to game
            self.game.paused = False                                                        #Just unpause
            return
        self.game.running = False                                                           #Else stop the game
        if(self.game.sent_from == "Menu"):                                                  #Then if you are playing the actual game
            self.game.save_to_file(self.game.player.lives, self.game.player.health)         #Save
            self.main_menu.change_screen("#FILES")                                          #Return to the file select screen
        else:                                                                               #Otherwise you came from the level editor
            self.main_menu.change_screen(self.game.file)                                    #So go back to the level editor
        
