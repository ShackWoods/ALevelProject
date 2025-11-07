###IMPORTS###
from Sprite import Sprite
import pygame
from Common_Functions import click_in_bounds
###Premade functions###
import glob
import csv

#A class to control what the editor is doing
class Editor_Controller:
    def __init__(self, menu_control):
        self.main_menu = menu_control

        border_img = pygame.image.load('Images/Border.png').convert_alpha()         #Load the border image
        focusA = Sprite((632,26), border_img)                                       #Instantiate sprites for the focuses
        focusB = Sprite((632,312), border_img)                                      #-These identify what tile and mode is selected
        self.focuses = [focusA, focusB]

        self.positions = {}
        self.img_dict = {}
        for filename in [image[7:] for image in glob.glob('Images/*')]:             #For each image file
            this_img = pygame.image.load(f"Images/{filename}").convert_alpha()      #Load the image
            self.img_dict[filename[:-4]] = this_img                                 #And store to the dictionary
        variants = ["R","U","L","D"]
        for i, var in enumerate(variants):                                          #Rotate the Oway image to produce the individual one-way platforms
            degrees = -90 + 90 * i                                                  #Determine the rotation amount
            rotated = pygame.transform.rotate(self.img_dict["Oway"], degrees)
            self.img_dict[f"{var}way"] = rotated

        self.active = False                                                         #Not active on initial load

    #A function to prepare a new csv file
    def new_file(self, name: str):
        temp_grid = [[""] * 240 for x in range(16)]                                 #Create a max_size blank grid
        with open(f"Levels/Custom/{name}.csv", "w", newline='') as newfile:         #Then write to the csv file
            writer = csv.writer(newfile)
            writer.writerows(temp_grid)

    #A function to initialise the variables
    def load(self, file, new_level = False):
        if(new_level):                                                              #Create a file for a new level
            self.new_file(file)
        self.file = file

        self.shift_focus((632,26), 0)                                               #Reset the tile and move
        self.shift_focus((632,312), 1)
        self.mode = "Draw"
        self.tile = "Floor"

        self.scroll = 0
        self.active = True
        self.player_pos = None                                                      #Must have 1 player
        self.flag_pos = None                                                        #and 1 flag
        self.previous_position = [-1,-1]
        self.grid = [[""] * 240 for x in range(16)]                                 #Create a grid for 10 screens of level <- for fast lookup
        with open(f"Levels/Custom/{self.file}.csv", "r") as lvlfile:                #Load the relevant file
            csv_reader = csv.reader(lvlfile)
            row_data = [row for row in csv_reader]
        for y, row in enumerate(row_data):                                          #Then add to the grid
            for x, tile in enumerate(row):
                self.grid[y][x] = tile
                if(tile == "Player"):                                               #Flagging the player and flag if they exist
                    self.player_pos = (x, y)
                elif(tile == "Flag"):
                    self.flag_pos = (x, y)
                    
        self.objects = [[None] * 240 for x in range(16)]                            #Create an array to store the objects <- for drawing
        for y, row in enumerate(self.grid):                                         #Instantiate a Sprite for each tile
            for x, tile in enumerate(row):
                if(tile == "Start"): continue                                       #Ignore the air tiles
                if(tile == ""): continue
                new_pos = (x * 32, y * 32)                                          #Determine the actual position
                new_img = self.img_dict[tile]                                       #And the relevant image
                new_obj = Sprite(new_pos, new_img)                                  #Then instantiate
                if(new_pos[0] > 576): new_obj.on_screen = False                     #Flag as off_screen if off screen
                self.objects[y][x] = new_obj                                        #Store to the array    

        self.hide_latch = False                                                     #A set of latches used for the keybinds
        self.hidden = False
        
        self.mode_latch = False
        self.erase_latch = False
        self.draw_latch = False
        
        self.tiles_latch = False
        self.entity_latch = False
        self.mods_latch = False
        
        self.left_latch = False
        self.right_latch = False

        self.palette = "Tiles"                                                      #Initialise the palette to Tiles
        self.p_pointer = 0

    #A function to save the file and change screen
    def unload(self, mode: list):
        self.active = False                                                         #Deactivate
        if(self.grid[0][0] == ""):                                                  #Ensure the first tile has a value (quirk of .csv format)
            self.grid[0][0] = "Start"

        #Trim empty columns (save space)
        empty_cols = [True] * 240
        for row in self.grid:                                                       #Loop through each tile to see which columns are empty
            for x, tile in enumerate(row):
                if(tile != ""):
                    empty_cols[x] = False
                    continue
                
        max_x = 24                                                                  #Ensure at least 1 screen exists
        for pos in range(239, 23, -1):                                              #Loop through each column (from the right)
            if(empty_cols[pos]): continue                                           #And find the first non_empty column
            max_x = pos + 1                                                         #Flag the first non_empty column
            break

        to_save = []
        for row in self.grid:
            to_save.append(row[:max_x])                                             #Slice each row to the size determined

        with open(f"Levels/Custom/{self.file}.csv", "w", newline='') as newfile:    #Then actually save
            writer = csv.writer(newfile)
            writer.writerows(to_save)
            
        if(mode[0] == "Save"):                                                      #If just saving:
            self.main_menu.change_screen("#LEVELS")                                 #Change the screen to the Level Select screen
        elif(self.player_pos is None or self.flag_pos is None):                     #Prevent testing a level without a player/flag
            print("You need a flag and a player")                                   #Feedback to the player the error
            self.active = True                                                      #Reactivate
        else:
            self.main_menu.change_screen(("#GAME",self.file), "Editor")             #Play the level, telling the GAME object to return to the editor

    #A function to change the position of a focus
    def shift_focus(self, position, focus):
        self.focuses[focus].position = position                                     #Just move the relevant focus
        self.previous_position = [-1,-1]                                            #And declare the last click as offscreen (used later)

    #A function to change the mode of the editor
    def change_mode(self, new_mode: str):
        self.mode = new_mode                                                        #Set the mode
        if(new_mode == "Erase"):                                                    #Then shift the focus accordingly
            self.shift_focus((704,312), 1)
        else:
            self.shift_focus((632,312), 1)
        self.previous_position = [-1,-1]                                            #And declare the last click as offscreen

    #A function to scroll the editor
    def change_scroll(self, amount: int):
        self.scroll += amount                                                       #Move
        self.scroll = max(0, self.scroll)                                           #Make sure we're not negative
        if(self.hidden):                                                            #If the palette is hidden:
            self.scroll = min(216, self.scroll)                                     #Can't scroll past 9 screens
            shift = 23                                                              #There are 24 tiles on screen
        else:
            self.scroll = min(221, self.scroll)                                     #Can't scroll past 9 screens and 5 tiles
            shift = 18                                                              #There are19 tiles on screen

        bounds = (self.scroll, self.scroll + shift)                                 #Determine what x positions are on screen
        for y in range(16):                                                         #Loop through each coordinate
            for x in range(240):
                obj = self.objects[y][x]
                if(obj is None): continue                                           #Ignoring empty tiles

                if(x < bounds[0] or x > bounds[1]):                                 #Flag off screen objects as off_screen
                    obj.on_screen = False
                else:
                    obj.on_screen = True                                            #And on screen objects as on_screen

    #An interface function between the palette and the editor
    def btn_clicked(self, button):
        action = button[0]
        match action:                                                               #Determine the button clicked and perform its action
            case "Draw": self.change_mode("Draw")
            case "Erase": self.change_mode("Erase")
            case "Left": self.change_scroll(-1)
            case "Right": self.change_scroll(1)
            case "LPalette": self.change_palette(-1)
            case "RPalette": self.change_palette(1)
            case _:                                                                 #In this case we are drawing a tile
                self.tile = action                                                  #So update the tile selected
                self.shift_focus(self.positions[action], 0)                         #And shift focus accordingly

    #A function to check the existance of the player/flag when the grid changes
    def revoke_core_objects(self, hovered_tile):
        if(hovered_tile == "Player"):                                               #The tile updated contained the player
            self.player_pos = None
        elif(hovered_tile == "Flag"):                                               #The tile updated contained the flag
            self.flag_pos = None

    #The function to keep the grid up to date
    def modify_grid(self):
        mouse_position = list(pygame.mouse.get_pos())                               #Deterime where the mouse is
        
        right_side = 607                                                            #Determine where the right side of the screen is
        if(self.hidden):                                                            #More screen available when the palette is hidden
            right_side = 767

        if(not click_in_bounds(mouse_position, [0, right_side, 0, 511])): return    #Check if the mouse is on_screen (ignores palette)
        if(click_in_bounds(mouse_position, [0, 127, 0, 63]) and not self.hidden):   #Ignore if the player is trying to save/play
            return
        
        current_position = [mouse_position[x] // 32 for x in range(2)]              #Convert mouse_position to grid indices
        current_position[0] += self.scroll                                          #And adjust to scroll
        if(current_position == self.previous_position): return                      #Only consider new clicks
        self.previous_position = current_position

        hovered_tile = self.grid[current_position[1]][current_position[0]]          #Then update the relevant tile
        self.revoke_core_objects(hovered_tile)                                      #Check if the flag/player was overwritten
        if(self.mode == "Erase"):                                                   #Erase if in erase mode
            self.grid[current_position[1]][current_position[0]] = ""
            self.objects[current_position[1]][current_position[0]] = None           #Garbage collection will delete an overwritten object
        else:                                                                       #Draw if in draw mode
            self.grid[current_position[1]][current_position[0]] = self.tile         #Set the grid to store the tile
            new_pos = (current_position[0] * 32, current_position[1] * 32)          #Determine the true position
            new_img = self.img_dict[self.tile]                                      #And image
            new_obj = Sprite(new_pos, new_img)                                      #To Instantiate a Sprite of the tile
            self.objects[current_position[1]][current_position[0]] = new_obj        #Then store to the object array
            if(self.tile == "Player"):                                              #Then flag the player
                if(self.player_pos is not None):                                    #Only allow one player at a time
                    self.grid[self.player_pos[1]][self.player_pos[0]] = ""          #So erase a duplicate
                    self.objects[self.player_pos[1]][self.player_pos[0]] = None
                self.player_pos = current_position                                  #Perform the flagging
            elif(self.tile == "Flag"):                                              #Repeat for the flag
                if(self.flag_pos is not None):
                    self.grid[self.flag_pos[1]][self.flag_pos[0]] = ""
                    self.objects[self.flag_pos[1]][self.flag_pos[0]] = None
                self.flag_pos = current_position

    #A function to actually run the editor each frame
    def run_frame(self, mouse_down):
        self.shortcuts()                                                            #Check if any shortcuts/keybinds were used
        if(mouse_down): self.modify_grid()                                          #Then update the grid if the mouse is down

        visible = []
        for row in self.objects:                                                    #Flag all the on_screen objects
            for obj in row:
                if(obj is None): continue
                if(not obj.on_screen): continue
                visible.append(obj)
        for vis in visible:                                                         #Then draw the on_screen objects
            vis.draw(self.main_menu.screen, self.scroll * 32)

    #A function to check if the player is using any shortcuts  
    def shortcuts(self):                                                            #No logic, just latching
        keys = pygame.key.get_pressed()                                             #Get a list of all keys pressed this frame

        if(keys[pygame.K_h]): self.hide_latch = True                                #Hide/show the save and play buttons as well as the palette
        else:
            if(self.hide_latch): self.hide_buttons(not self.hidden)
            self.hide_latch = False
            
        if(keys[pygame.K_m]): self.mode_latch = True                                #Alternate the mode
        else:
            if(self.mode_latch):
                if(self.mode == "Draw"): self.change_mode("Erase")
                else: self.change_mode("Draw")
            self.mode_latch = False

        if(keys[pygame.K_e]): self.erase_latch = True                               #Set mode to Erase
        else:
            if(self.erase_latch): self.change_mode("Erase")
            self.erase_latch = False

        if(keys[pygame.K_d]): self.draw_latch = True                                #Set mode to Draw
        else:
            if(self.draw_latch): self.change_mode("Draw")
            self.draw_latch = False

        if(keys[pygame.K_1]): self.tiles_latch = True                               #Change palette to the Tiles palette
        else:
            if(self.tiles_latch): self.change_palette("Tiles")
            self.tiles_latch = False

        if(keys[pygame.K_2]): self.entity_latch = True                              #Change palette to the Entitites palette
        else:
            if(self.entity_latch): self.change_palette("Entities")
            self.entity_latch = False

        if(keys[pygame.K_3]): self.mods_latch = True                                #Change palette to the Mods palette
        else:
            if(self.mods_latch): self.change_palette("Mods")
            self.mods_latch = False

        if(keys[pygame.K_LEFT]): self.left_latch = True                             #Scroll left
        else:
            if(self.left_latch): self.change_scroll(-1)
            self.left_latch = False
            
        if(keys[pygame.K_RIGHT]): self.right_latch = True                           #Scroll right
        else:
            if(self.right_latch): self.change_scroll(1)
            self.right_latch = False

    #A function to adjust the screen when hidden
    def hide_buttons(self, new_state):       
        self.hidden = new_state                                                     #Update the hide flag
        if(self.scroll == 221 and self.hidden):                                     #If hiding and at the end of the file
            self.change_scroll(-5)                                                  #Move forward 5 tiles
        elif(self.scroll == 216 and not self.hidden):                               #If unhiding and at the end of the file
            self.change_scroll(5)                                                   #Move back 5 tiles
        else:
            self.change_scroll(0)                                                   #Make sure that tiles behind the palette are revealed

    #A function to change the palette
    def change_palette(self, target):
        self.hide_buttons(False)                                                    #Unhide the buttons
        palettes = ["Tiles", "Entities", "Mods"]                                    #A list of palette options
        palette_primaries = ["Floor", "Player", "SHeal"]                            #A list of the first tile in each palette
        if(type(target) is str):                                                    #If directly updating (the target is known)
            self.palette = target                                                   #Update the palette
            self.p_pointer = palettes.index(target)                                 #And move the pointer
        else:                                                                       #Else you're "scrolling" the palettes
            self.p_pointer += target                                                #Determine the next palette
            self.p_pointer = self.p_pointer % 3
            self.palette = palettes[self.p_pointer]                                 #And update accordingly
        self.tile = palette_primaries[self.p_pointer]                               #Update the selected tile to reflect the palette
        self.shift_focus(self.positions[self.tile], 0)                              #Then shift focus accordingly
        
