#The base class of all visual elements
#stores the information needed to draw the object to the correct part of the screen
class Sprite:
    def __init__(self, position: tuple, image):
        self.position = list(position)                                      #Position refers to the top-left corner
        self.image = image
        self.size = (self.image.get_width(), self.image.get_height())       #Size should reflect the image size in pixels
        self.on_screen = True

    #Function to draw the Sprite onto a surface (typically the screen)
    def draw(self, surface, shift = 0):
        relative_position = [self.position[0] - shift, self.position[1]]    #Adjust the image position if necessary
        surface.blit(self.image, relative_position)                         #Then draw
