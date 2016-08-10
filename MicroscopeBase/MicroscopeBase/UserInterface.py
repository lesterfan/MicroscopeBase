import pygame
import time
import colors
import printfunctions
import gameobjects

DEFAULT_OUT_OF_SCREEN_VALUE = 100000

class UserInterface:

    """ This class encapsulates the functions to read user input, to show user location, to save/load locations, 
        to deal with joystick inputs, and more... """

    # Defining self variables
    FPS = 0                                   # Internal Pygame variable
    Clock = None                              # Internal Pygame variable
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


    display_width = 330                       # Internal Pygame variable
    display_height = 425                      # Internal Pygame variable
   
    pygame_display = None                     # Reference to pygame display

    using_joystick = False                    # Will automatically be set based on if a joystick is connected when the program starts
    joystick = None                           # Reference to joystick object

    saved_positions = {}                      # Saved position is a hash : key = string, value = tuple (x,y)
    GUIButton_dict = {}

    message1 = ""                             # Message to show the user
    
    microscope_position_GUIobject = None      # GUI object for the microscope
    a_position_GUIobject          = None      # GUI object for the a button
    x_position_GUIobject          = None      # GUI object for the x button
    y_position_GUIobject          = None      # GUI object for the y button
    b_position_GUIobject          = None      # GUI object for the b button
    home_position_GUIobject       = None      # GUI object for the home button


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

        # Initialize pygame GUI objects to show where things are
        self.microscope_position_GUIobject = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.white)
        self.a_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.green) 
        self.x_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.blue)  
        self.y_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.yellow)
        self.b_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.red)   
        self.home_position_GUIobject       = gameobjects.Enemy(0, 0, 10, 10, colors.hot_pink)   

        # Place the GUIObjects for buttons into a dictionary to retrieve
        self.GUIButton_dict['a'] = self.a_position_GUIobject
        self.GUIButton_dict['x'] = self.x_position_GUIobject
        self.GUIButton_dict['y'] = self.y_position_GUIobject
        self.GUIButton_dict['b'] = self.b_position_GUIobject



    '''
    Initializes the self.joystick variable and maps the button nums to their respective positions
    '''
    def initialize_joystick(self, a_button_num = 0, x_button_num = 3, y_button_num = 4,
                            b_button_num = 1, rb_button_num = 7, start_button_num = 11, rt_button_num = 9):
                                
        pygame.joystick.init()

        if pygame.joystick.get_count() != 0:
            self.message1 = "Joystick mode activated!"
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
            self.message1 = "No joystick found! Joystick mode deactivated"


    ''' 
    Reads whatever keyboard key is being inputted. Allows for the interface to check if keys[pygame.K_x] is pressed
    '''
    def check_keyboard_keys(self):
        self.keys = pygame.key.get_pressed()


    '''
    Checks if the user leaves a key in the keyboard. Returns True if key_up, False otherwise
    '''
    def check_keyboard_key_up(self):
       for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                return True
       return False


    '''
    The next few functions get the positions of the joysticks
    '''

    def get_joystick_xfine(self):
        return self.joystick.get_axis(0)
    
    def get_joystick_yfine(self):
        return self.joystick.get_axis(1)

    def get_joystick_x(self):
        return self.joystick.get_axis(2)

    def get_joystick_y(self):
        return self.joystick.get_axis(3)




    '''
    Sets the value of self.a_button, self.x_button, etc. for this specific frame.
    '''
    def check_joystick_button(self):
        self.a_button     =     self.joystick.get_button      (  self.a_button_num      )
        self.x_button     =     self.joystick.get_button      (  self.x_button_num      )
        self.y_button     =     self.joystick.get_button      (  self.y_button_num      )
        self.b_button     =     self.joystick.get_button      (  self.b_button_num      )
        self.rb_button    =     self.joystick.get_button      (  self.rb_button_num     )
        self.start_button =     self.joystick.get_button      (  self.start_button_num  )
        self.rt_button    =     self.joystick.get_button      (  self.rt_button_num     )

    
    '''
    Saves the position of button string_input using Microscope_Base_Input
    @ param string_input : String that describes which button we're saving, eg. 'a', 'x', ...
    @ param Microscope_Base_Input : Microscope Base object that we're dealing with
    '''
    def save_position_to_button(self, string_input, Microscope_Base_Input):
        # Put the tuple in the dictionary
        absolute_position = Microscope_Base_Input.get_absolute_position()
        self.saved_positions[string_input] = absolute_position

        # Place the GUI marker down.
        x, y = absolute_position
        self.GUIButton_dict[string_input].xstart = int( x / 2000 ) 
        self.GUIButton_dict[string_input].ystart = int( y / 2000 )

    '''
    Loads the position of button string_input using Microscope_Base_Input
    @ param string_input : String that describes which button we're saving, eg. 'a', 'x', ...
    @ param Microscope_Base_Input : Microscope Base object that we're dealing with
    '''
    def load_position_from_button(self, string_input, Microscope_Base_Input):
        if string_input not in self.saved_positions:
            self.message1 = "Error! No position saved for "+string_input+" yet!"
        else:
            load_x, load_y = self.saved_positions[string_input]
            Microscope_Base_Input.x_move_abs(load_x)
            Microscope_Base_Input.y_move_abs(load_y)
            self.message1 = "Successfully loaded position to "+string_input


    '''
    Refreshes the pygame display according to the information in the rest of this class

    '''
    def refresh_pygame_display(self, Microscope_Base_Input):
        # Fill with pretty colors
        self.pygame_display.fill(colors.black)
        pygame.draw.rect(self.pygame_display, colors.white, [0, 333, 330, 100])
        pygame.draw.rect(self.pygame_display, colors.red, [0, 333, 330, 10])

        # Get absolute position to print
        absolute_location = Microscope_Base_Input.get_absolute_position()
        x, y = absolute_location

        # Draw the home location as well as the saved GUI marker objects
        self.home_position_GUIobject.drawToScreen()
        for key in self.GUIButton_dict:
            self.GUIButton_dict[key].drawToScreen()

        # Draw the microscope object according to current absolute location
        self.microscope_position_GUIobject.xstart = int( x / 2000 ) 
        self.microscope_position_GUIobject.ystart = int( y / 2000 )
        self.microscope_position_GUIobject.drawToScreen()

        # Print messages to screen
        printfunctions.message_to_screen("Location : "+str(absolute_location), colors.black, y_displace = 150, size = 'medium')
        printfunctions.message_to_screen(self.message1,colors.black, y_displace = 170)
        printfunctions.message_to_screen("RB + X,Y,B to save a position. Press X,Y,B to return to that", colors.black, y_displace = 185)
        printfunctions.message_to_screen("position. A to home.", colors.black, y_displace = 195)

        
        pygame.display.update()
        self.Clock.tick(self.FPS)