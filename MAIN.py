###IMPORTS###
import pygame
import sys
###UI Modules###
import Home_Screen_UI
import Files_Screen_UI
import Levels_Screen_UI
import Delete_Screen_UI
import Control_Screen_UI
import Editor_Tip_Screen_UI as ETSUI
import Editor_Screen_UI
from Game_Screen_UI import Game_UI
###Logic Modules###
import GAME
import EDITOR


#A class to display the relevant objects (the driver object)
class Menu_Controller:
    def __init__(self):
        pygame.init()                                                                               #Create a window                                     
        pygame.display.set_caption("GAME GAME")
        self.screen = pygame.display.set_mode((768, 512))
        self.clock = pygame.time.Clock()
        
        self.change_screen("#HOME")                                                                 #Load the home screen
        self.game = GAME.Game_Controller(self)                                                      #Instantiate the logic modules
        self.game_ui = Game_UI(self.game)
        self.editor = EDITOR.Editor_Controller(self)
        self.editor_ui = Editor_Screen_UI.Editor_UI(self.editor)

    #A function to delete a save file
    def delete_save(self, args):
        for part in self.active_UI:                                                                 #Find the textbox object
            try:
                answer = part.get_message()
                captcha = part.base_message
            except: pass
            
        if(captcha == answer):                                                                      #Determine if the captcha was correct
            file = args[0]
            
            saves = open("save_data.txt", "r").read().split("\n")                                   #If so load the save data
            this_save = "new, 5, 10, -1"                                                            #Delete the relevant save
            saves[file] = this_save

            f = open("save_data.txt", "w")                                                          #Then store to the file
            f.write("\n".join(saves))
            f.close()

        self.change_screen("#FILES")

    #A function to load the platformer
    def run_game(self, context, caller):
        self.game.load_file(context, caller)                                                        #Just load the platformer
        self.active_UI = []

    #Sets the UI elements and passes "control"
    def change_screen(self, target, caller = "Menu"):
        if(type(target) is tuple or type(target) is list):                                          #Split the arguments if necessary
            args = target[1:]
            target = target[0]
            
        match target:                                                                               #Load the relevant screen
            case "#HOME":
                self.active_UI = Home_Screen_UI.generate_UI(self.change_screen)
            case "#FILES":
                self.active_UI = Files_Screen_UI.generate_UI(self.change_screen)
            case "#LEVELS":
                self.active_UI = Levels_Screen_UI.generate_UI(self.change_screen)
            case "#GAME":
                self.run_game(args[0], caller)
            case "#DELETE":
                self.active_UI = Delete_Screen_UI.generate_UI(self.change_screen, self.delete_save)
            case "#CONTROLS":
                self.active_UI = Control_Screen_UI.generate_UI(self.change_screen)
            case "#TIPS":
                if(args[0] == "Buttons"):                                                           #The editor has two tip screens
                    self.active_UI = ETSUI.generate_buttons_UI(self.change_screen)
                else:
                    self.active_UI = ETSUI.generate_keybinds_UI(self.change_screen)
            case "#NEW GAME":
                name = ""
                marked_part = None
                for part in self.active_UI:                                                         #Find the Textbox
                    try:
                        name = part.get_message()                                                   #And check if a username was passed
                        marked_part = part
                    except: pass
                if(name == ""):                                                                     #If not
                    marked_part.base_message = "Input a name first"                                 #Update the textbox
                    marked_part.change_focus(True)
                    return
                self.game.new_file(name, args[0])                                                   #Else create a new file
                self.run_game(args[0], caller)                                                      #And run the game
            case "#NEW LEVEL":
                name = ""
                marked_part = None
                for part in self.active_UI:                                                         #Same thing as #NEW GAME
                    try:                                                                            #Make sure a level name was given
                        name = part.get_message()
                        marked_part = part
                    except: pass
                if(name == ""):
                    marked_part.base_message = "Input a name first"
                    marked_part.change_focus(True)
                    return
                self.editor.load(name, new_level = True)                                            #And only load if so
            case _:                                                                                 #The default case is to load a
                self.editor.load(target)                                                            #custom level of the passed name

    #A function to monitor for clicks
    def click_event(self, mouse_engaged: bool):
        mouse_position = list(pygame.mouse.get_pos())                                               #Determine where the click is
        for part in self.active_UI:                                                                 #And for each object
            try: part.clicked(mouse_engaged, mouse_position)                                        #Try to perform clicked function
            except: pass                                                                            #But ignore non buttons

    #A function to pass a Textbox keyboard inputs
    def listener(self, part, keys):
        part.del_timer = max(0, part.del_timer - 1)                                                 #Decrement the backpace timer
        for key in keys:                                                                            #Then for each key press
            part.listen(key)                                                                        #Pass the key to the Textbox

    #The main driver loop
    def in_control(self):
        '''
        On loop:
        Display the active elements
        Manage UI
        '''
        self.running = True
        pause_started = False
        mouse_down = False
        while self.running:                                                                         #MAINLOOP
            key_buffer = []
            for event in pygame.event.get():                                                        #For each pygame event
                if(event.type == pygame.MOUSEBUTTONDOWN):                                           #If the left mouse is down
                    if(event.button == 1):
                        mouse_down = True                                                           #Flag mouse as down
                        self.click_event(mouse_down)                                                #Run click event
                if(event.type == pygame.MOUSEBUTTONUP):                                             #If the left mouse is up
                    if(event.button == 1):
                        mouse_down = False                                                          #Flag mouse as up
                        self.click_event(mouse_down)                                                #Run click event
                if(event.type == pygame.KEYDOWN):                                                   #If a key was pressed
                    key_buffer.append(pygame.key.name(event.key))                                   #Add to the buffer
                if(event.type == pygame.QUIT):                                                      #If the game was exited
                    pygame.display.quit()                                                           #Close the game
                    sys.exit()

            self.screen.fill((50,50,50))                                                            #Clear the screen

            if(self.game.running):                                                                  #If the game is running
                if(not self.game.paused):                                                           #And unpaused
                    self.game_ui.generate_main_ui()                                                 #Load the unpaused UI
                    self.active_UI = self.game_ui.main_UI
                    pause_started = False
                elif(not pause_started):                                                            #Else if paused and it is the first pause frame
                    self.game_ui.generate_pause_ui()                                                #Load the paused UI
                    self.active_UI = self.game_ui.pause_UI
                    pause_started = True
                self.game.run_frame()                                                               #Then run the game

            if(self.editor.active):                                                                 #If the editor is active
                self.editor.run_frame(mouse_down)                                                   #Monitor for mouse presses
                self.active_UI = self.editor_ui.assemble()                                          #And load the relevant UI

            for part in self.active_UI:                                                             #For each UI element
                part.draw(self.screen)                                                              #Overlay it
                try:
                    part.listen("")                                                                 #Then "listen" if it is a Textbox
                    self.listener(part, key_buffer)
                except: pass
                
            pygame.display.flip()                                                                   #Draw to the screen

            self.clock.tick(60)                                                                     #Then tick 1 60th of a second

if __name__ == "__main__":                                                                          #Only run if this file was the initial file
    controller = Menu_Controller()                                                                  #Instantiate the controller
    controller.in_control()                                                                         #And begin the driver code
