###IMPORTS###
###Assets###
from Sprite import Sprite
import Crawler
import Flyer
import Walker
import Platforms as P
import Player
import Consumables as C
###Premade functions
import csv
import pygame
import time
import glob


#A class to store the methods and variables needed to run the platformer
class Game_Controller:
    def __init__(self, menu_control):
        self.main_menu = menu_control
        self.file = None
        self.running = False
        self.paused = False
        self.pause_latch = False
        self.sent_from = "Menu"
        self.max_level = len(glob.glob('Levels/Built_In/*.csv'))                                    #Determines the number of levels that exist

    #A function to create a new save
    def new_file(self, name, file: int):    
        saves = open("save_data.txt", "r").read().split("\n")                                       #Load the save files
        this_save = f"{name}, 5, 10, 1"                                                             #Update the relevant row
        saves[file] = this_save

        f = open("save_data.txt", "w")                                                              #Then rewrite to the file
        f.write("\n".join(saves))
        f.close()

    #Auxiliary function to free up memory
    def clear_game(self):
        self.grid = None
        self.graph_info = None
        self.tiles = None
        self.flag = None
        self.tile_colliders = None
        self.player = None
        self.crawlers = None        
        self.flyers = None        
        self.walkers = None
        self.hitboxes = []

    #A function to load a level
    def load_file(self, file, sent_from: str):
        self.sent_from = sent_from
        self.clear_game()
        self.scroll = 0
        
        #Loading screen
        self.main_menu.screen.fill((0,0,0))                                                         #Fill the screen with black
        pygame.display.flip()
        time.sleep(1)                                                                               #And stall for 1 second
        
        self.file = file
        self.running = True
        self.paused = False
        
        #Load File
        if(self.sent_from == "Menu"):                                                               #Loads a built_in level
            this_save = open("save_data.txt", "r").read().split("\n")[file]
            player_info = [int(x) for x in this_save.split(", ")[1:3]]
            this_level = this_save.split(", ")[3]
            level_file = f"Levels/Built_In/{this_level}.csv"
        else:                                                                                       #Loads a custom level
            player_info = [1, 10]
            level_file = f"Levels/Custom/{file}.csv"

        #Read Level File
        with open(level_file, "r") as lvlfile:                                                      #Actually read the level file
            csv_reader = csv.reader(lvlfile)
            row_data = [row for row in csv_reader]

        #Gridify
        to_generate = {"Player":[], "Flag":[],                                                      #Create a dictionary for each object
                       "Crawler":[], "Walker":[], "Flyer":[],
                       "Floor":[], "Honey":[], "Spike":[],
                       "Uway":[], "Dway":[], "Lway":[], "Rway":[],
                       "SHeal":[], "MHeal":[], "LHeal":[],
                       "DJump":[], "WJump":[], "DStrike":[],
                       "Run":[], "Dash":[]}
        self.grid = [[""]*len(row_data[0]) for i in range(len(row_data))]                           #And a blank array for the grid
        for y,row in enumerate(row_data):                                                           #For each tile
            for x,tile in enumerate(row):
                if(tile == "Start"): continue                                                       #Ignore non_solid objects
                if(tile != ""): to_generate[tile].append((x,y))
                if(tile in ["Player","Flag","Crawler","Walker","Flyer"]):                           #Treat the entities as non_solid objects
                    tile = ""
                self.grid[y][x] = tile                                                              #Store the platform type to the grid
        level_bound = len(self.grid[0]) * 32
        self.camera_edge = level_bound - 768

        ROWS = len(self.grid)                                                                       #Set and group these constants for later use
        COLS = len(self.grid[0])
        self.graph_info = (ROWS, COLS)

        #GENERATE OBJECTS - Tiles, Entities      
        img_dict = {}
        for filename in [image[7:] for image in glob.glob('Images/*')]:                             #For each image file
            this_img = pygame.image.load(f"Images/{filename}").convert_alpha()                      #Load the image
            img_dict[filename[:-4]] = this_img                                                      #And store to the dictionary

        ##TILES
        self.tiles = []
        for position in to_generate["Floor"]:                                                       #For each floor:
            true_position = [position[0] * 32, position[1] * 32]                                    #Find the in game position
            new_floor = P.Std_Platform(true_position, img_dict["Floor"])                            #Instantiate an object
            self.tiles.append(new_floor)                                                            #Store to the list
            
        for position in to_generate["Honey"]:                                                       #Repeat for each honey tile
            true_position = [position[0] * 32, position[1] * 32]
            new_honey = P.Honey_Platform(true_position, img_dict["Honey"])
            self.tiles.append(new_honey)
            
        for position in to_generate["Spike"]:                                                       #And for each spike
            true_position = [position[0] * 32, position[1] * 32]
            new_spike = P.Spike_Platform(true_position, img_dict["Spike"])
            self.tiles.append(new_spike)
            
        for position in to_generate["Uway"]:                                                        #And for each upwards one_way
            true_position = [position[0] * 32, position[1] * 32]
            new_uway = P.One_Way_Platform(true_position, img_dict["Oway"], "down")
            self.tiles.append(new_uway)
            
        for position in to_generate["Dway"]:                                                        #And do mostly the same for downwards one_ways
            true_position = [position[0] * 32, position[1] * 32]
            img = pygame.transform.rotate(img_dict["Oway"], 180)                                    #Just rotating the one_way image accordingly
            new_dway = P.One_Way_Platform(true_position, img, "up")
            self.tiles.append(new_dway)
            
        for position in to_generate["Lway"]:                                                        #Repeat the new method for left one_ways
            true_position = [position[0] * 32, position[1] * 32]
            img = pygame.transform.rotate(img_dict["Oway"], 90)
            new_lway = P.One_Way_Platform(true_position, img, "right")
            self.tiles.append(new_lway)
            
        for position in to_generate["Rway"]:                                                        #And then for right one_ways
            true_position = [position[0] * 32, position[1] * 32]
            img = pygame.transform.rotate(img_dict["Oway"], 270)
            new_rway = P.One_Way_Platform(true_position, img, "left")
            self.tiles.append(new_rway)

        flag_position = (to_generate['Flag'][0][0] * 32, to_generate['Flag'][0][1] * 32)            #Determine where the flag is
        self.flag = P.Flag(flag_position, img_dict["Flag"])                                         #And instantiate the flag object
        self.tiles.append(self.flag)                                                                #Then add to the list

        self.tile_colliders = [pygame.Rect(tile.position, tile.size) for tile in self.tiles]        #Then create a collider for all the tiles

        ##ENTITIES
        player_pos = [to_generate["Player"][0][0] * 32, to_generate["Player"][0][1] * 32]           #Determine where the player is
        lives = player_info[0]                                                                      #And the lives/health
        health = player_info[1]
        self.player = Player.Player(player_pos, img_dict["Player"], lives, health, level_bound)     #Instantiate the Player object
        
        self.crawlers = []
        for position in to_generate["Crawler"]:                                                     #For each Crawler:
            true_position = [position[0] * 32, position[1] * 32]                                    #Find the in_game position
            new_crawler = Crawler.Crawler(true_position, img_dict["Crawler"], self.grid)            #Then instantiate the Crawler
            try:
                if(new_crawler.destroy_flag): continue                                              #This is a check to remove trapped/floating crawlers
            except:
                pass
            self.crawlers.append(new_crawler)                                                       #Then add to the crawler list

        self.flyers = []
        for position in to_generate["Flyer"]:                                                       #Repeat for all flyers
            true_position = [position[0] * 32, position[1] * 32]
            new_flyer = Flyer.Flyer(true_position, img_dict["Flyer"], self.player)
            self.flyers.append(new_flyer)
        
        self.walkers = []
        for position in to_generate["Walker"]:                                                      #And then for all walkers
            true_position = [position[0] * 32, position[1] * 32]
            new_walker = Walker.Walker(true_position, img_dict["Walker"], self.player, level_bound)
            self.walkers.append(new_walker)

        ##CONSUMABLES/MODS
        self.consumables = []
        heal_amounts = [1,2,5]
        for x, heal in enumerate(["SHeal", "MHeal", "LHeal"]):                                      #For each heal type
            for position in to_generate[heal]:                                                      #For each instance of that type
                true_position = [position[0] * 32, position[1] * 32]                                #Find the in game position
                new_heal = C.Heal(true_position, img_dict[heal], self.player, heal_amounts[x])      #Instantiate a Heal object
                self.consumables.append(new_heal)                                                   #And add to the list

        for upgrade in ["DJump", "WJump", "DStrike", "Run", "Dash"]:                                #Then repeat for each upgrade type
            for position in to_generate[upgrade]:
                true_position = [position[0] * 32, position[1] * 32]
                new_upgrade = C.Upgrade(true_position, img_dict[upgrade], self.player, upgrade)
                self.consumables.append(new_upgrade)

        self.timer = 6060                                                                           #100 second level with 1 grace second

    #The driver code for the game controller
    def run_frame(self):
        keys = pygame.key.get_pressed()                                                             #Determine what keys were pressed

        ##Pause logic
        if(keys[pygame.K_p]): self.pause_latch = True                                               #Perform the pause latch
        else:
            if(self.pause_latch):
                self.paused = not self.paused                                                       #Changing state if necessary
            self.pause_latch = False
        
        self.draw_game()                                                                            #Always draw the game            
        if(self.paused): return                                                                     #And end the frame early if paused

        ##Move
        movementKeys = (keys[pygame.K_UP] or keys[pygame.K_w],                                      #Check the movement keys
                        keys[pygame.K_LEFT] or keys[pygame.K_a],
                        keys[pygame.K_RIGHT] or keys[pygame.K_d],
                        keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
        self.movement(movementKeys)                                                                 #Then perform movement for all entities

        ##Level clear check
        if(self.flag.complete):                                                                     #Check if the level flag was hit
            self.draw_game()                                                                        #Make sure the player can see they hit the flag
            if(self.sent_from == "Menu"):                                                           #If actually playing the game
                self.save_to_file(self.player.lives, self.player.health, level_shift = 1)           #Progress to the next level
                self.forced_draw()
                time.sleep(1)
            self.load_file(self.file, self.sent_from)                                               #Then load the file again
            return                                                                                  #Ending the frame early

        ##Timer check
        self.timer -= 1                                                                             #Decrement the timer
        if(self.timer <= 0):                                                                        #If timer falls to 0
            self.player.lives -= 1                                                                  #Lose a life
            self.reset(False)                                                                       #And reset
            return                                                                                  #Ending the frame early

        ##Consumable logic
        self.resolve_consumables()                                                                  #Perform the function

        ##Attack logic
        attacks = self.gather_attacks(keys[pygame.K_SPACE])                                         #Gather all the attacks
        self.resolve_attacks(attacks)                                                               #And then resolve them

        ##Hitbox logic
        to_destroy = []
        for x, hitbox in enumerate(self.hitboxes):                                                  #For each hitbox to draw
            hitbox.timer -= 1                                                                       #Reduce its timer
            if(hitbox.timer < 0):                                                                   #Flagging hitboxes with a timer < 0
                to_destroy.insert(0, x)
            else:
                hitbox.draw(self.main_menu.screen)                                                  #And drawing the others
        for index in to_destroy:                                                                    #Then for each flagged hitbox
            this_hitbox = self.hitboxes.pop(index)                                                  #Remove the reference
            del this_hitbox                                                                         #Then delete the object

        ##Update FSMs
        fsms = [f.fsm for f in self.flyers] + [w.fsm for w in self.walkers]                         #Group the objects with FSM's
        for fsm in fsms: fsm.change_state()                                                         #And update their state

        ##On_screen checks
        self.on_screen()                                                                            #Finally, check which objects are on screen

    #A function to draw the game
    def draw_game(self):
        visible_tiles = [tile for tile in self.tiles if tile.on_screen]                             #Determine which tiles are visisble
        entities = self.consumables + self.crawlers + self.flyers
        entities = entities + self.walkers + [self.player] + [self.flag]
        visible_entities = [entity for entity in entities if entity.on_screen]                      #And which entities are visible
        
        for visible in visible_tiles:                                                               #Draw the visible tiles
            visible.draw(self.main_menu.screen, self.scroll)

        for visible in visible_entities:                                                            #Then for each visible entitiy
            try:
                if((visible.invulnerable // 5) % 2 == 1): continue                                  #Flash if invulnerable
            except: pass
            visible.draw(self.main_menu.screen, self.scroll)                                        #Else draw       

    #A function to force the screen to update mid frame
    def forced_draw(self):
        self.main_menu.screen.fill((50,50,50))                                                      #Clear the screen
        self.draw_game()                                                                            #Draw the game
        pygame.display.flip()                                                                       #Then show it

    #A function to run the movement function of each entity
    def movement(self, player_keys: list):
        self.player.controller(player_keys, self.tiles, self.tile_colliders)
        for crawler in self.crawlers: crawler.logic(self.tile_colliders)
        for walker in self.walkers: walker.logic(self.grid, self.tiles, self.tile_colliders)         
        for flyer in self.flyers: flyer.interpret_fsm(self.grid, self.graph_info)

    #A function to determine what consumables have been touched by the player
    def resolve_consumables(self):
        touched = []
        for x, consumable in enumerate(self.consumables):                                           #For each consumable
            if(consumable.touch_check()):                                                           #Flag the ones which were touched
                touched.insert(0, x)
                
        for deletion in touched:                                                                    #Then for each flagged object
            target = self.consumables.pop(deletion)                                                 #Remove any reference to the object
            del target                                                                              #And delete the object

    #A function to gather the attacks of all combatant objects
    def gather_attacks(self, player_key: bool) -> list:
        attacks = []
        if(player_key): attacks = self.player.attack(attacks, facing = self.player.facing)          #If the player attacks, run the player attack
        for crawler in self.crawlers:                                                               #For each crawler
            attacks = crawler.attack(attacks)                                                       #Try to attack
        for flyer in self.flyers:                                                                   #For each flyer
            attacks = flyer.attack(attacks)                                                         #Try to attack
        for walker in [w for w in self.walkers if w.fsm.current_state == "attacking"]:              #For each attacking walker
            attacks = walker.attack(attacks, facing = walker.facing)                                #Try to attack
        return attacks

    #A function to actually deal damage and remove dead objects
    def resolve_attacks(self, attack_list: list):
        enemies = self.walkers + self.flyers + self.crawlers                                        #Group the enemy type objects
        dead_list = []
        for packet in attack_list:                                                                  #Packet format: Hitbox, Attacker
            hitbox = packet[0]
            attacker = packet[1]
            damage = attacker.weapon_damage
            player_team = attacker.is_player_team
            draw_hitbox = attacker.draw_hitbox

            if(draw_hitbox):                                                                        #If the hitbox is to be drawn
                position = (hitbox.left + self.scroll, hitbox.top)                                  #Determine its position
                image = pygame.Surface((hitbox.width, hitbox.height))                               #Create a red square
                image.fill((255,0,0))
                new_hitbox = Sprite(position, image)                                                #Instantiate a Sprite object
                new_hitbox.timer = 6                                                                #Start a 6 frame counter
                self.hitboxes.append(new_hitbox)                                                    #And save to the hitbox list

            if(player_team): attackable = enemies                                                   #Prevent enemies hurting enemies
            else: attackable = [self.player]
            
            for opponent in attackable:                                                             #For each opponent
                collider = pygame.Rect(opponent.position, opponent.size)                            #Create their collider
                if(not pygame.Rect.colliderect(collider, hitbox)): continue                         #Test for a collision

                is_dead = opponent.damaged(damage)                                                  #Deal damage
                if(is_dead): dead_list.append(opponent)                                             #And if dead, flag
                
        for combatant in enemies + [self.player]:                                                   #For each combatant
            combatant.invulnerable = max(combatant.invulnerable - 1, 0)                             #Decrement their invulnerable timer
            combatant.locked = max(combatant.locked - 1, 0)                                         #And decrement their attack lock timer

        if(self.player.position[1] > 512): self.reset(True)                                         #If the player is off_screen, reset
        if(self.player.health <= 0): self.reset(False)                                              #If the player is dead, reset
           
        for dead in dead_list:                                                                      #For each dead object, remove all references
            for x, flyer in enumerate(self.flyers):
                if(flyer != dead): continue
                del self.flyers[x]
            for x, walker in enumerate(self.walkers):
                if(walker != dead): continue
                del self.walkers[x]
            for x, crawler in enumerate(self.crawlers):
                if(crawler != dead): continue
                del self.crawlers[x]
            if(self.player == dead):
                self.reset(False)                                                                   #Don't delete the player, just reset
                break
            del dead                                                                                #Then delete the object

    #A function to update a save file
    def save_to_file(self, lives: int, health: int, level_shift = 0):
        saves = open("save_data.txt", "r").read().split("\n")                                       #Read the relevant file
        this_save = saves[self.file].split(", ")

        level = int(this_save[3]) + level_shift
        if(level > self.max_level):                                                                 #Stop the game from loading a
            print("Congratulations, you have beaten GAME GAME :D")                                  #non_existant level (the game has been beaten)
            level = int(this_save[3])

        alternate_save = [this_save[0], str(lives), str(health), str(level)]                        #Group the updated save info
        saves[self.file] = ", ".join(alternate_save)

        f = open("save_data.txt", "w")                                                              #Then save to the file
        f.write("\n".join(saves))
        f.close()

    #A function to reset the level
    def reset(self, screen_death: bool):
        self.forced_draw()                                                                          #Force the game to draw
        def silly(shift: int):                                                                      #Auxiliary function to just play an animation
            self.player.move(0,shift)
            self.forced_draw()
            time.sleep(0.01)

        self.running = False                                                                        #Stop running the game
        if(screen_death):                                                                           #Determine which type of death happened
            self.player.lives -= 1                                                                  #In off screen, the player loses a life
            self.player.position[1] = 480                                                           #Reposition the player
            self.forced_draw()                                                                      #Prevent smearing of the player
            toRise = 0
            toFall = 32
        else:
            toRise = 16
            toFall = (544 - self.player.position[1]) // 4

        time.sleep(1)                                                                               #Pause to let player reflect
        for a in range(toRise):                                                                     #Then play the animation
            silly(-2)
        for b in range(toFall):
            silly(4)
        time.sleep(1)

        if(self.sent_from == "Editor"):                                                             #Reload the level if sent from the editor
            self.load_file(self.file, self.sent_from)
            return

        if(self.player.lives <= 0):                                                                 #Else check for a game over
            self.save_to_file(5, 10)                                                                #Reseting the lives and health if so
            self.main_menu.change_screen("#HOME")                                                   #And sending back to the home screen
            return

        self.save_to_file(self.player.lives, 10)                                                    #Otherwise save and reset  
        self.load_file(self.file, self.sent_from)

    #A function to determine which objects are on screen
    def on_screen(self):
        margin = [self.scroll + 128, self.scroll + 640]                                             #Determine the margins of the screen
        left_conditions = self.player.facing == "left" and self.scroll > 0                          #Determine if a left scroll is possible
        if(self.player.position[0] < margin[0] and left_conditions):                                #If moving into the left margin
            self.scroll = max(0,self.player.position[0] - 128)                                      #Scroll as far left as possible
            
        right_conditions = self.player.facing == "right" and self.scroll < self.camera_edge         #Determine if a right scroll is possible
        if(self.player.position[0] > margin[1] and right_conditions):                               #If moving into the right margin
            self.scroll = min(self.camera_edge, self.player.position[0] - 640)                      #Scroll as far right as possible

        screen_bounds = [self.scroll - 128, self.scroll + 896]                                      #Determine the bounds of the screen
        objects = self.tiles + [self.flag] + [self.player]                                          #Group all the objects
        objects = objects + self.crawlers + self.flyers + self.walkers
        for obj in objects:                                                                         #For each object
            if(obj.position[0] < screen_bounds[0] or obj.position[0] > screen_bounds[1]):           #Check if on screen
                obj.on_screen = False
            else: obj.on_screen = True
