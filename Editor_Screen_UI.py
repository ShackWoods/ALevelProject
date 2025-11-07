###IMPORTS###
from Sprite import Sprite
from Button import Button
import pygame

#Some UI turns on and off depending on the state of the editor, hence the class
class Editor_UI:
    def __init__(self, editor_control):
        self.editor = editor_control                                                            #The current object used for the editor section

        self.meta = self.generate_meta_buttons()                                                #Functions to generate each UI element by type
        self.static = self.generate_static_buttons()
        self.tiles = self.generate_tile_palette()
        self.entities = self.generate_entity_palette()
        self.mods = self.generate_mod_palette()

    #Generates the buttons which allow the user to change game states
    def generate_meta_buttons(self) -> list:
        '''
        META Elements:
        -Save button
        -Play button
        '''
        save_img = pygame.image.load('Images/save.png').convert()                               #Load the save and play button images
        play_img = pygame.image.load('Images/play.png').convert()
        
        btnSave = Button((0,0), save_img, self.editor.unload, "Save")                           #Instantiate the save and play buttons
        btnPlay = Button((64,0), play_img, self.editor.unload, "Play")
        return [btnSave, btnPlay]                                                               #Return the button objects

    #Generates the buttons which appear on all 3 palettes
    def generate_static_buttons(self) -> list:
        '''
        Static Elements:
        -Mode change buttons
        -Scroll buttons
        -Change palette buttons
        '''       
        draw_img = pygame.image.load('Images/Draw.png').convert()                               #Load the images for the draw, erase
        erase_img = pygame.image.load('Images/Erase.png').convert()                             #scroll, and palette change buttons
        scroll_img = pygame.image.load('Images/Arrow.png').convert_alpha()
        palette_scroll_img = pygame.image.load("Images/Palette_Arrow.png").convert_alpha()

        rotated_scroll_img = pygame.transform.rotate(scroll_img, 180)                           #Rotate the two scroll images to use for
        rotated_ps_img = pygame.transform.rotate(palette_scroll_img, 180)                       #a left-pointing arrow

        btnDraw = Button((636,316), draw_img, self.editor.btn_clicked, "Draw")                  #Instantiate all the buttons
        btnErase = Button((708,316), erase_img, self.editor.btn_clicked, "Erase")
        btnRight = Button((708,388), scroll_img, self.editor.btn_clicked, "Right")
        btnLeft = Button((636,388), rotated_scroll_img, self.editor.btn_clicked, "Left")
        btnRPalette = Button((708,460), palette_scroll_img, self.editor.btn_clicked, "RPalette")
        btnLPalette = Button((636,460), rotated_ps_img, self.editor.btn_clicked, "LPalette")
        return [btnDraw, btnErase, btnRight, btnLeft, btnRPalette, btnLPalette]                 #Return the button objects

    #Generic function to generate the palettes
    def generate_palette(self, colour: tuple, btns_to_make: list) -> list:
        '''
        Generic Palette Elements:
        -Background
        -Button for each "tile" type
        '''
        palette_img = pygame.Surface((160,512))                                                 #Generate a background image for the palette
        palette_img.fill(colour)
        palette = Sprite((608,0), palette_img)                                                  #Instantiate the image as a Sprite

        object_btns = []

        oway_img = pygame.image.load('Images/Oway.png').convert()                               #One-Ways use the same image for
                                                                                                #different directions of one-way
        for i, element in enumerate(btns_to_make):                                              #Loop through each button
            match element:                                                                      #Test for which image should be loaded
                case "Uway": img = oway_img                                                     #Up oway uses the base oway image           
                case "Lway": img = pygame.transform.rotate(oway_img, 90)                        #Left oway is roated 90 degrees CW
                case "Dway": img = pygame.transform.rotate(oway_img, 180)                       #Down oway is a flipped image
                case "Rway": img = pygame.transform.rotate(oway_img, -90)                       #Right oway is rotated 90 degrees ACW
                case _: img = pygame.image.load(f'Images/{element}.png').convert_alpha()        #All other objects have different images
            x = 636 + (i % 2) * 72                                                              #Determine the relevant x and y positions
            y = 30 + (i // 2) * 72
            btn = Button((x,y), img, self.editor.btn_clicked, element)                          #Instantiate the button object
            self.editor.positions[element] = (x - 4, y - 4)                                     #These are the positions for the "focuses"
            object_btns.append(btn)                                                             #Add new object to the list

        return [palette] + object_btns                                                          #Return a list of the palette and buttons

    #Specific function to generate the "tile palette"
    def generate_tile_palette(self) -> list:
        btns_to_make = ["Floor","Uway",                                                         #Just a list of the different buttons
                        "Honey","Lway",                                                         #on this palette
                        "Spike","Dway",
                        "Flag","Rway"]

        return self.generate_palette((55, 76, 255), btns_to_make)                               #Call the generic function

    #Specific function to generate the "entity palette"
    def generate_entity_palette(self) -> list: 
        btns_to_make = ["Player","Walker",                                                      #Just a list of the buttons on this palette
                        "Crawler","Flyer"]

        return self.generate_palette((237,84,144), btns_to_make)                                #Call the generic function

    #Specific function to generate the "modification palette"
    def generate_mod_palette(self) -> list:
        btns_to_make = ["SHeal","DJump",                                                        #Just a list of the buttons on this palette
                        "MHeal","WJump",
                        "LHeal","DStrike",
                        "Run","Dash"]

        return self.generate_palette((26,214,88), btns_to_make)                                 #Call the generic function
        
    #Select the relevant elements to be displayed
    def assemble(self) -> list:
        current_UI = []

        match self.editor.palette:                                                              #Selects the relevant palette
            case "Tiles":
                current_UI += self.tiles
            case "Entities":
                current_UI += self.entities
            case "Mods":
                current_UI += self.mods
                
        current_UI += self.static                                                               #Add the static and meta UI
        current_UI += self.meta
        current_UI += self.editor.focuses                                                       #Add the "focuses" to show what is
                                                                                                #currently selected
        if(not self.editor.hidden):                                                             #Only display if not hidden
            return current_UI
        
        return []
