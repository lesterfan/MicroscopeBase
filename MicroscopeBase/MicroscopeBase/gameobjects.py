import pygame
import time
import random
import colors
import os
#pygame.init()

#display_width = 800
#display_height = 600
#gameDisplay = pygame.display.set_mode((display_width,display_height))
#smallfont = pygame.font.SysFont("comicsansms",25)
#mediumfont = pygame.font.SysFont("comicsansms",50)
#largefont = pygame.font.SysFont("comicsansms",80)
#clock = pygame.time.Clock()
#
#cdisplayStartX = 3*display_width / 8
#cdisplayStartY = 4*display_height / 8
#cdisplayWidth = display_width / 4
#FPS = 60

DISPLAY_WIDTH = 640                               # The microscope goes from 0 to 640k
DISPLAY_HEIGHT = 768                              # The microscope goes from 0 to 768k
LOCATION_HEIGHT = 100
INSTRUCTION_HEIGHT = 100
MICROSCOPE_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+LOCATION_HEIGHT + INSTRUCTION_HEIGHT))

class Enemy:
    
    def __init__(self, xstart, ystart, enemyWidth, enemyHeight, color, img = ""):
        self.xstart = xstart
        self.ystart = ystart
        self.enemyWidth = enemyWidth
        self.enemyHeight = enemyHeight
        self.color = color
        self.img = img 
        self.microscope_x = 0
        self.microscope_y = 0
        if self.img != "":
            self.image = pygame.image.load(os.path.join(self.img))
            self.image.convert()
       


    def drawToScreen(self, gameDisplay):
        if self.img == "":
            pygame.draw.rect(gameDisplay, self.color, [self.xstart, self.ystart, self.enemyWidth, self.enemyHeight])
        else:
            gameDisplay.blit(self.image,[self.xstart,self.ystart])
    

