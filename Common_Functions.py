###IMPORTS###
import pygame
from math import sqrt as root

#Calculates the pythagorean distance between two points
def pythagorus(positionA, positionB, scalar = 1) -> int:                                #It's just pythagorus
    x_distance = positionA[0] - positionB[0]
    y_distance = positionA[1] - positionB[1]
        
    square_md = (x_distance ** 2) + (y_distance ** 2)
    true_md = root(square_md)
    return round(true_md * scalar)                                                      #Scale, then return as an integer

#Determines if a point lies within some set of bounds
def click_in_bounds(mouse_position: list, bounds: tuple) -> bool:                       #Guard clauses will reject invalid clicks
    if(mouse_position[0] < bounds[0]): return False                                     #Mouse x < object left
    if(mouse_position[0] > bounds[1]): return False                                     #Mouse x > object right
    if(mouse_position[1] < bounds[2]): return False                                     #Mouse y < object top
    if(mouse_position[1] > bounds[3]): return False                                     #Mouse y > object bottom
    return True                                                                         #Not bad -> good :D

#Converts a string into a rectangular image
def text_to_image(font, text: str, bold: bool, fg_colour: tuple, bg_colour = (0,0,0)):
    txt = font.render(text, bold, fg_colour)                                            #Premade function to convert a text to an image
    image = pygame.Surface((txt.get_width(), txt.get_height()))                         #Create a drawable object for the image
    image.fill(bg_colour)                                                               #Fill with the background colour
    image.blit(txt, (0,0))                                                              #Then draw the image onto the background
    return image
