import pygame
import time
import colors


class UserInterface:

    """ This class encapsulates the functions to read user input, to show user location, to save/load locations, 
        to deal with joystick inputs, and more... """

    # Defining self variables
    FPS = 0                                   # Internal Pygame variable
    Clock = None                              # Internal Pygame variable
    unit_change = 1000                        # Internal Pygame variable
    keys = None                               # Internal Pygame variable

    a_button =  0                             # Internal Pygame variable
    x_button =  0                             # Internal Pygame variable
    y_button =  0                             # Internal Pygame variable
    b_button =  0                             # Internal Pygame variable
    rb_button = 0                             # Internal Pygame variable
    start_button = 0                          # Internal Pygame variable
    rt_button = 0                             # Internal Pygame variable

    display_width = 320                       # Internal Pygame variable
    display_height = 484                      # Internal Pygame variable
   

    using_joystick = False                    # Will automatically be set based on if a joystick is connected when the program starts
    joystick = None                           # Reference to joystick object


    x_change = 0                              # Change in x location on a given frame
    y_change = 0                              # Change in y location on a given frame
    x = 0                                     # Current x position in a given frame
    y = 0                                     # Current y position in a given frame

    message1 = ""                             # Message to show the user
    
    def __init__(self, pygame_title = "HMNL (c) 2016: All rights reserved."):

        # Initialize pygame / joystick
        pygame.init()                        
        pygame.joystick.init()

        if pygame.joystick.get_count() != 0:

            self.using_joystick = True


    def initialize_joystick(self, joystick_num = 0):

        joystick = pygame.joystick.Joystick(joystick_num)

