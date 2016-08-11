import pygame
import time
import colors
import printfunctions
import gameobjects
import dotnet.seamless


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
    lt_button = 0                             # Internal Pygame variable

    a_button_num = 0                          # Which joystick numbers should be checked internally
    x_button_num = 0                          # Which joystick numbers should be checked internally
    y_button_num = 0                          # Which joystick numbers should be checked internally
    b_button_num = 0                          # Which joystick numbers should be checked internally
    rb_button_num = 0                         # Which joystick numbers should be checked internally
    start_button_num = 0                      # Which joystick numbers should be checked internally
    rt_button_num = 0                         # Which joystick numbers should be checked internally
    lt_button_num = 0                         # Which joystick numbers should be checked internally


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

    mAnalyzer = None


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
        self.a_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.blue) 
        self.x_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.hot_pink)  
        self.y_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.green)
        self.b_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.orange)   
        self.home_position_GUIobject       = gameobjects.Enemy(0, 0, 10, 10, colors.red)   

        # Place the GUIObjects for buttons into a dictionary to retrieve
        self.GUIButton_dict['a'] = self.a_position_GUIobject
        self.GUIButton_dict['x'] = self.x_position_GUIobject
        self.GUIButton_dict['y'] = self.y_position_GUIobject
        self.GUIButton_dict['b'] = self.b_position_GUIobject


        
        # Load the compiled C# library to analyze the microscope with.
        dotnet.add_assemblies('C:\\Users\\HMNL\\Desktop\\VsGithub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase\\')
        dotnet.load_assembly('MicroscopeAnalyzerLibrary')
        import MicroscopeAnalyzerLibrary

        # Creates the MicroscopeAnalyzer object from the loaded C# library
        self.mAnalyzer = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer(True)


    '''
    Initializes the self.joystick variable and maps the button nums to their respective positions
    '''
    def initialize_joystick(self, a_button_num = 0, x_button_num = 3, y_button_num = 4,
                            b_button_num = 1, rb_button_num = 7, start_button_num = 11, rt_button_num = 9, lt_button_num = 8):

        pygame.joystick.quit()

        pygame.joystick.init()

        if pygame.joystick.get_count() != 0:
            self.message1 = "Joystick found! Joystick mode activated!"
            self.using_joystick = True

            # Setting up the internal joystick nums
            self.a_button_num         =  a_button_num    
            self.x_button_num         =  x_button_num    
            self.y_button_num         =  y_button_num    
            self.b_button_num         =  b_button_num    
            self.rb_button_num        =  rb_button_num   
            self.start_button_num     =  start_button_num 
            self.rt_button_num        =  rt_button_num   
            self.lt_button_num        =  lt_button_num   

            # Initialize the joystick
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        else:
            self.using_joystick = False
            self.message1 = "No joystick found! Joystick mode deactivated!"


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
        return self.joystick.get_axis(2)
    
    def get_joystick_yfine(self):
        return self.joystick.get_axis(3)

    def get_joystick_x(self):
        return self.joystick.get_axis(0)

    def get_joystick_y(self):
        return self.joystick.get_axis(1)

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
        self.lt_button    =     self.joystick.get_button      (  self.lt_button_num     )

    
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
    Moves Microscope_Base_Input num amount of microns on the x axis, given that 6.4 microsteps = 1 um. Will round to the nearest microstep.
    @ param num : number of microns
    Returns : None
    '''
    def x_move_microns(self, num, Microscope_Base_Input):
        Microscope_Base_Input.x_move_rel(int( round( num * 6.4 ) ))

    '''
    Moves Microscope_Base_Input num amount of microns on the y axis, given that 6.4 microsteps = 1 um. Will round to the nearest microstep.
    @ param num : number of microns
    Returns : None
    '''
    def y_move_microns(self, num, Microscope_Base_Input):
        Microscope_Base_Input.y_move_rel(int( round( num *6.4 ) ))

    '''
    Moves Microscope_Base_Input num amount of mm on the x axis, given that 6400 microsteps = 1 mm.
    @ param num : number of mm
    Returns : None
    '''
    def x_move_mm(self, num, Microscope_Base_Input):
        Microscope_Base_Input.x_move_rel( num * 6400 )

    '''
    Moves Microscope_Base_Input num amount of mm on the y axis, given that 6400 microsteps = 1 mm.
    @ param num : number of mm
    Returns : None
    '''
    def y_move_mm(self, num, Microscope_Base_Input):
        Microscope_Base_Input.y_move_rel( num * 6400 )


    '''
    Takes a measurement. Recipe must be set and baseline must be taken
    '''
    def take_measurement(self):
        self.message1 = "Now measuring!"
        self.mAnalyzer.Measure()

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


    '''
    Takes a map. For now, only accepts odd number of points
    @ param mapping name : The prefix that all the files of this map will be saved as.
    @ param numPointsX : number of points desired on the x-axis
    @ param DistancebwPointsX : desired distance b/w points on the x-axis
    @ param numPointsY : number of points desired on the y-axis
    @ param DistancebwPointsY : desired distance b/w points on the y-axis
    @ param units : desired units, 'um' or 'mm'
    @ param Microscope_Base_Input : reference to the microscope base object on which to move
    '''
    def take_map(self, mapping_name, numPointsX, DistancebwPointsX, numPointsY, DistancebwPointsY, units, Microscope_Base_Input):
        
        # Check that all the inputs are integral
        if not (numPointsX % 1 == 0 or DistancebwPointsX % 1 == 0 or numPointsY % 1 == 0 or DistancebwPointsY % 1 == 0):
            self.message1 = "Error! Please make sure everything is integral!"


        # Check that numPointsX, numPointsY only accepts odd inputs
        if numPointsX % 2 == 0 or numPointsY % 2 == 0:
            self.message1 = "Please enter in an ODD number of points on the x/y axes!"
            return

        xPointsRadius = int((numPointsX - 1)/2)                                           # Will always be integral, so cast it straight away
        yPointsRadius = int((numPointsY - 1)/2)                                           # Will always be integral, so cast it straight away


        # Set the moving function according to the units entered
        move_x = None
        move_y = None
        if units == 'um':
            move_x = self.x_move_microns
            move_y = self.y_move_microns
        elif units == 'mm':
            move_x = self.x_move_mm
            move_y = self.y_move_mm
        else:
            self.message1 = "Invalid units!"
            return


        # Save the center position to return to at the end
        self.saved_positions['CENTER'] = Microscope_Base_Input.get_absolute_position()


        # Move to the extreme top left of the user defined grid
        move_x(-1*int(xPointsRadius * DistancebwPointsX), Microscope_Base_Input)
        move_y(-1*int(yPointsRadius * DistancebwPointsY), Microscope_Base_Input)


        # Update display to provide a real time view of the map
        self.refresh_pygame_display(Microscope_Base_Input)


        # Performs map going up to down, left to right in that order.
        for i in range(numPointsX):

            # If not the first column, then move back up and move right
            if i != 0:
                move_x(DistancebwPointsX, Microscope_Base_Input)
                move_y(-1*(numPointsY)*(DistancebwPointsY), Microscope_Base_Input)

            for j in range(numPointsY):

                # Take a measurement.
                print "Now measuring"
                self.take_measurement()

                # The next few lines save this measuremnet

                print "Now saving!"
                desired_file_name = mapping_name + "_{0}_{1}".format(i,j)
                currFileDir = "C:/Users/HMNL/Documents/Test/"

                # Save the .fmspe file into its own folder.
                self.mAnalyzer.SaveSpectrum(currFileDir + "FMSPE/", desired_file_name)

                # Save the .xml file into its own folder
                self.mAnalyzer.SaveResultsTo(currFileDir + "XML/", desired_file_name)

                # Save the image file into its own folder
                self.mAnalyzer.SaveImageTo(currFileDir + "Images/", desired_file_name)

                # Move down
                move_y(DistancebwPointsY, Microscope_Base_Input)

                # Update display to provide a real time view of the map
                self.refresh_pygame_display(Microscope_Base_Input)


        # After the map is over, return the base to its center location
        self.load_position_from_button('CENTER', Microscope_Base_Input)