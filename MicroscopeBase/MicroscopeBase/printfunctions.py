import pygame
import time
import random
import colors
pygame.init()


display_width = 320                               # The microscope goes from 0 to 640k
display_height = 484                            # The microscope goes from 0 to 768k

gameDisplay = pygame.display.set_mode((display_width, display_height))
smallfont = pygame.font.SysFont("comicsansms",10)
mediumfont = pygame.font.SysFont("comicsansms",20)
largefont = pygame.font.SysFont("monospace",80)
clock = pygame.time.Clock()

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text,True,color)
    if size == "medium":
        textSurface = mediumfont.render(text,True,color)
    if size == "large":
        textSurface = largefont.render(text,True,color)
    return textSurface, textSurface.get_rect()


#y_displace is the displacement from the center
def message_to_screen(msg, color, y_displace = 0, size = "small", x_displace = 0):
    textSurf, textRect = text_objects(msg, color,size)
    textRect.center = (display_width/2) + x_displace, (display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)




