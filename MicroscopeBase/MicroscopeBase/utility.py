import pygame
import time
import random
import colors
pygame.init()

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
smallfont = pygame.font.SysFont("comicsansms",20)
mediumfont = pygame.font.SysFont("monospace",30)
largefont = pygame.font.SysFont("monospace",80)
clock = pygame.time.Clock()


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(colors.white)
        message_to_screen("Statics RPG",
                          colors.green,
                          -120,
                          "large")
        message_to_screen("This is a prototype of the game.",
                          colors.black,
                          -60)
        message_to_screen("You, the main character, fell down from SERC into an alternative universe...",
                          colors.black,
                          -10)
        message_to_screen("And now you must go through an adventure to escape!",
                          colors.black,
                          30)
        message_to_screen("Note: This version is without sound. I highly suggest playing music while playing.",
                          colors.black,
                          50)
        message_to_screen("Press C to play or Q to quit",
                          colors.black,
                          180)
        pygame.display.update()
        clock.tick(5)

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




