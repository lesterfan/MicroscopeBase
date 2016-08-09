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

    a_button_num = 0                          # Which joystick numbers should be checked internally
    x_button_num = 0                          # Which joystick numbers should be checked internally
    y_button_num = 0                          # Which joystick numbers should be checked internally
    b_button_num = 0                          # Which joystick numbers should be checked internally
    rb_button_num = 0                         # Which joystick numbers should be checked internally
    start_button_num = 0                      # Which joystick numbers should be checked internally
    rt_button_num = 0                         # Which joystick numbers should be checked internally


    display_width = 320                       # Internal Pygame variable
    display_height = 484                      # Internal Pygame variable
   
    pygame_display = None                     # Reference to pygame display

    using_joystick = False                    # Will automatically be set based on if a joystick is connected when the program starts
    joystick = None                           # Reference to joystick object


    x_change = 0                              # Change in x location on a given frame
    y_change = 0                              # Change in y location on a given frame
    x = 0                                     # Current x position in a given frame
    y = 0                                     # Current y position in a given frame

    message1 = ""                             # Message to show the user
    

    ''' 
    Constructor that sets up connection to user interface. Instantiates all the 
    internal variables
    @ param pygame_title : String that shows the text that should be displayed
    Returns None
    '''
    def __init__(self, pygame_title = "HMNL (c) 2016: All rights reserved."):

        # Initialize pygame / joystick
        pygame.init()

        # Setting up pygame internal variables
        self.FPS = 60
        self.Clock = pygame.time.Clock()
        self.pygame_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption(pygame_title)


    '''
    Initializes the self.joystick variable and maps the respective button nums to their rightful
    positions 
    '''
    def initialize_joystick(self, a_button_num, x_button_num, y_button_num,
                            b_button_num, rb_button_num, start_button_num, rt_button_num):
                                
        pygame.joystick.init()

        if pygame.joystick.get_count() != 0:
            print "Using joystick!"
            self.using_joystick = True

            # Setting up the internal joystick nums
            self.a_button_num         =  a_button_num    
            self.x_button_num         =  x_button_num    
            self.y_button_num         =  y_button_num    
            self.b_button_num         =  b_button_num    
            self.rb_button_num        =  rb_button_num   
            self.start_button_num     =  start_button_num 
            self.rt_button_num        =  rt_button_num   

            # Initialize the joystick
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        else:
            print "Not using joystick!"
            

    '''
    Refreshes the display after each frame.
    Call on each loop.
    '''
    def refresh_display(self):
        pygame.display.update()
        self.Clock.tick(self.FPS)

    ''' 
    Reads whatever key is being inputted. Call before running any of the checker functions
    '''
    def get_keys(self):
        self.keys = pygame.key.get_pressed()

    
    '''
    The next few functions detect specific keyboard inputs described by their name
    '''

    def left_key_pressed(self):
        if self.keys[pygame.K_LEFT]:
            return True
        else:
            return False

    def right_key_pressed(self):
        if self.keys[pygame.K_RIGHT]:
            return True
        else:
            return False

    def down_key_pressed(self):
        if self.keys[pygame.K_DOWN]:
            return True
        else:
            return False
        
    # def right_key_pressed(self):
    #     if self.keys[pygame.K_UP]:
    #         return True
    #     else:
    #         return False
    #     
    # def right_key_pressed(self):
    #     if self.keys[pygame.K_RIGHT]:
    #         return True
    #     else:
    #         return False