import pygame
import time
import colors
import printfunctions
import gameobjects
import dotnet.seamless
import os
from random import randint

# Load the compiled C# library with which to interact with the Filmmetrics software
# dotnet.add_assemblies('C:\\Users\\HMNL\\Desktop\\VsGithub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase\\')
# dotnet.load_assembly('MicroscopeAnalyzerLibrary')
# import MicroscopeAnalyzerLibrary

DEFAULT_OUT_OF_SCREEN_VALUE = 100000

class UserInterface:

    """ This class encapsulates the functions to read user input, to show user location, to save/load locations, 
        to deal with joystick inputs, and more... """

    # Defining self variables
    FPS = 0                                   # Internal Pygame variable
    Clock = None                              # Internal Pygame variable
    keys = None                               # Internal Pygame variable

    lx_axis = -1                              # Internal Pygame variable
    ly_axis = -1                              # Internal Pygame variable
    trigger_axis = -1                         # Internal Pygame variable
    rx_axis = -1                              # Internal Pygame variable
    ry_axis = -1                              # Internal Pygame variable

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

    display_width = 1230                       # Internal Pygame variable
    display_height = 325                      # Internal Pygame variable
   
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

    gui_app = None
    gui_container = None

    mAnalyzer = None

    dummy_mode = False

    # Internal variables to be read from the GUI
    joystick_selected = ""
    fmspe_dir = ""
    xml_dir = ""
    image_dir = ""
    map_name = ""
    units = ""
    update_joystick_pressed = False
    single_measurement_pressed = False
    pause_button_pressed = False
    stop_button_pressed = False
    quit_button_pressed = False

    # Pictures that add color to the GUI
    dino_image = None

    ''' 
    Constructor that sets up connection to user interface. Instantiates all the 
    internal variables
    @ param pygame_title : String that shows the text that should be displayed
    Returns None
    '''
    def __init__(self, dummy_mode = False, pygame_title = "HMNL (tm) 2016: All rights reserved."):

        if dummy_mode:
            self.dummy_mode = True

        # Initialize pygame / joystick
        pygame.init()

        # Setting up pygame internal variables
        self.FPS = 60
        self.Clock = pygame.time.Clock()
        self.pygame_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption(pygame_title)



        # Initialize pygame GUI objects to show where things are
        self.microscope_position_GUIobject = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.black   , img = "Sprites/HMNL_sprite.png")
        self.a_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.blue    , img = "Sprites/a_button_sprite.png") 
        self.x_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.hot_pink, img = "Sprites/x_button_sprite.png")  
        self.y_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.green   , img = "Sprites/y_button_sprite.png")
        self.b_position_GUIobject          = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.orange  , img = "Sprites/b_button_sprite.png")   
        self.home_position_GUIobject       = gameobjects.Enemy(500, 0, 10, 10, colors.red                                                       , img = "Sprites/home_position_sprite.png")   

        # Place the GUIObjects for buttons into a dictionary to retrieve
        self.GUIButton_dict['a'] = self.a_position_GUIobject
        self.GUIButton_dict['x'] = self.x_position_GUIobject
        self.GUIButton_dict['y'] = self.y_position_GUIobject
        self.GUIButton_dict['b'] = self.b_position_GUIobject

        # Creates the MicroscopeAnalyzer object from the loaded C# library
        if not self.dummy_mode:
            self.mAnalyzer = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer(True)

        self.set_theme()
        
    '''
    Initializes the theme of the GUI
    '''
    def set_theme(self):
        #pics_list = ["dino_pic.jpg", "jordan_pic.jpg", "keg_pic.jpg", "lamborghini_pic.jpg", "machop_pic.jpg", "nitzsche_pic.jpg", "snoopy_pic.jpg", "zubats_sketch.jpg", "minato_pic.jpg", "snorlax_pic.jpg"]
        pics_list=["buttonmap_fit.png"]
        # Loading up the colorful pictures
        self.dino_image = pygame.image.load(os.path.join(pics_list[randint(0,len(pics_list)-1)]))
        self.dino_image.convert()



    '''
    Initializes the self.joystick variable and maps the button nums to their respective positions
    '''
    def initialize_joystick(self, a_button_num = 0, x_button_num = 3, y_button_num = 4,
                            b_button_num = 1, rb_button_num = 7, start_button_num = 11, 
                            lx_axis = 0, ly_axis = 1, trigger_axis = None, rx_axis = 2, ry_axis = 3,
                            rt_button_num = 9, lt_button_num = 8):

    # For da other joystick : def initialize_joystick(self, a_button_num = 0, x_button_num = 2, y_button_num = 3,
    # For da other joystick :                         b_button_num = 1, rb_button_num = 5, start_button_num = 7, 
    # For da other joystick :                         lx_axis = 0, ly_axis = 1, trigger_axis = 2, rx_axis = 3, ry_axis = 4, 
    # For da other joystick :                         rt_button_num = None, lt_button_num = None):

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
            self.lx_axis              =  lx_axis
            self.ly_axis              =  ly_axis
            self.trigger_axis         =  trigger_axis
            self.rx_axis              =  rx_axis
            self.ry_axis              =  ry_axis

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
    Checks if the user leaves a key in the keyboard. Returns True if key_up, False otherwise, in addition, sends events to the GUI.
    '''
    def check_keyboard_key_up(self):
       for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                return True

            if event.type == pygame.QUIT:
                self.quit_button_pressed = True
            else:
                self.quit_button_pressed = False

            self.gui_app.event(event)
       return False


    '''
    The next few functions get the positions of the joysticks and if the buttons are pressed
    '''

    def get_joystick_xfine(self):
        return self.joystick.get_axis(self.rx_axis)
    
    def get_joystick_yfine(self):
        return self.joystick.get_axis(self.ry_axis)

    def get_joystick_x(self):
        return self.joystick.get_axis(self.lx_axis)

    def get_joystick_y(self):
        return self.joystick.get_axis(self.ly_axis)

    def check_rt_button_pressed(self):
        if self.rt_button_num !=  None:
            return self.joystick.get_button      (  self.rt_button_num     )
        else:
            if self.joystick.get_axis(self.trigger_axis) <= -1*0.07:
                return 1
            else:
                return 0

    def check_lt_button_pressed(self):
        if self.lt_button_num != None:
            return self.joystick.get_button      (  self.lt_button_num     )
        else:
            if self.joystick.get_axis(self.trigger_axis) >= 0.07:
                return 1
            else:
                return 0

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

        # On one controller the triggers are buttons, but on the other, the triggers are an axis. We control for that here.
        self.rt_button    =     self.check_rt_button_pressed()
        self.lt_button    =     self.check_lt_button_pressed()


    
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
        self.GUIButton_dict[string_input].xstart = int( x / 2000 ) + 500
        self.GUIButton_dict[string_input].ystart = int( y / 2000 )

        # Change the message display
        self.message1 = "Successfully saved position to button "+string_input

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
    Sets the internal GUI objects to the user defined guiApp and guiContainer
    '''
    def set_gui(self, guiApp, guiContainer):
        self.gui_app = guiApp
        self.gui_container = guiContainer

    '''
    Refreshes the pygame display according to the information in the rest of this class
    '''
    def refresh_pygame_display(self, Microscope_Base_Input = None):
        # Fill with pretty colors
        self.pygame_display.fill(colors.white)
        # pygame.draw.rect(self.pygame_display, colors.black, [500, 0, 330, 325])
        self.pygame_display.blit(self.dino_image, (500,0))

        # Get absolute position to print
        if not self.dummy_mode:
            absolute_location = Microscope_Base_Input.get_absolute_position()
            x, y = absolute_location
        else:
            # Place dummy values on the x and y
            x = 10
            y = 10

        # Draw the home location as well as the saved GUI marker objects
        self.home_position_GUIobject.drawToScreen(self.pygame_display)
        for key in self.GUIButton_dict:
            self.GUIButton_dict[key].drawToScreen(self.pygame_display)

        # Draw the microscope object according to current absolute location
        self.microscope_position_GUIobject.xstart = int( x / 2000 ) + 500
        self.microscope_position_GUIobject.ystart = int( y / 2000 )
        self.microscope_position_GUIobject.drawToScreen(self.pygame_display)

        # Refresh / render GUI
        self.gui_app.paint()
        self.gui_app.update()


        # Print messages to screen
        printfunctions.message_to_screen("Units in um", colors.red,    y_displace = 110, x_displace = -365, size = 'small')
        printfunctions.message_to_screen("Location : ({},{})".format(format(x*0.15625,'.5f'),format(y*0.15625,'.5f')), colors.black, y_displace = 125, x_displace = -365, size = 'medium')
        printfunctions.message_to_screen(self.message1,colors.black,                         y_displace = 145, x_displace = -365)
        
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
    @ param currFileDir : string that represents the directory in which the map data will be saved.
    '''
    def take_map(self, mapping_name, numPointsX, DistancebwPointsX, numPointsY, DistancebwPointsY, units, Microscope_Base_Input): 
        
        self.message1 = "Now taking a map!"

        # Check that all the inputs are integral
        if not (numPointsX % 1 == 0 or DistancebwPointsX % 1 == 0 or numPointsY % 1 == 0 or DistancebwPointsY % 1 == 0):
            self.message1 = "Error! Please make sure everything is integral!"
            return


        # If the entered amount is odd, the exact center will be measured along with the spectrum. If it's even, then the center won't be measured, but
        # the software will measure AROUND the center.
        xPointsRadius = int((numPointsX - 1)/2)                                           
        yPointsRadius = int((numPointsY - 1)/2)                                           


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

                # The next few lines save this measuremnet with an x,y location stamp on it.
                print "Now saving!"
                x, y = Microscope_Base_Input.get_absolute_position()
                desired_file_name = mapping_name + "_x{0}_y{1}".format(x,y)

                # Save the .fmspe file into its own folder.
                self.mAnalyzer.SaveSpectrum(self.gui_container.fmspe_dir_input.value, desired_file_name)

                # Save the .xml file into its own folder
                self.mAnalyzer.SaveResultsTo(self.gui_container.xml_dir_input.value, desired_file_name)

                # Save the image file into its own folder
                self.mAnalyzer.SaveImageTo(self.gui_container.image_dir_input.value, desired_file_name)

                # Move down
                move_y(DistancebwPointsY, Microscope_Base_Input)

                # Check the GUI to see if the pause button has been clicked
                self.check_keyboard_key_up()

                # Check joystick to see if LT (pause has been clicked)
                self.check_joystick_button()

                # If the stop button is clicked, return the base to its center location, set the flag back to False, and exit
                if self.stop_button_pressed:
                    self.load_position_from_button('CENTER', Microscope_Base_Input)
                    self.stop_button_pressed = False
                    self.message1 = "Map stopped!"
                    return

                # If the pause button is clicked, then pause it indefinitely until the user clicks it again
                if self.pause_button_pressed or self.lt_button == 1:
                    self.pause_button_pressed = False
                    while True:
                        self.message1 = "Map paused! Press start/pause to resume, stop to terminate!"
                        self.check_keyboard_key_up()
                        self.check_joystick_button()

                        # If they click the pause button again, breaks out of this infinite loop
                        if self.pause_button_pressed or self.lt_button == 1:
                            self.pause_button_pressed = False
                            break

                        # If they click the stop button, returns from the mapping function
                        if self.stop_button_pressed:
                            self.load_position_from_button('CENTER', Microscope_Base_Input)
                            self.stop_button_pressed = False
                            return

                        self.refresh_pygame_display(Microscope_Base_Input)

                # Update display to provide a real time view of the map
                self.refresh_pygame_display(Microscope_Base_Input)


        # After the map is over, return the base to its center location
        self.load_position_from_button('CENTER', Microscope_Base_Input)

    '''
    Takes in a directory of where the .xml files are saved in the map, output directory,
    and the map name, and saves a .txt file containing the neat information of the analysis_items
    in the output file
    @ param xml_dir : string representing the directory of the .xml files
    @ param output_dir : string representing the directory of the desired output .txt file
    @ param map_name : string representing the name of the map the user saved
    @ analysis_items : dictionary object representing the items needed to analyze
    '''
    def PostProcessAndSave(self, xml_dir, output_dir, map_name, analysis_items):
        # Fill up a list of strings with the relevant .xml files!
        xml_files = [filename for filename in os.listdir(xml_dir) if filename.startswith(map_name) and filename.endswith(".xml")]
        
        if len(xml_files) == 0:
            self.message1 = "Error in checkout! Invalid name!"
            return

        # Open the output .txt file to write
        output_txt_file = open(output_dir + "Analysis_" + map_name + ".txt", 'w')

        # Parse through the files and take out the important information, and write it
        for file in xml_files:
            result = MicroscopeAnalyzerLibrary.MicroscopeAnalyzer.LoadResultsFrom(xml_dir + file)

            # If it's the first iteration, write the labels at the top first
            if file == xml_files[0]:
                 output_txt_file.write("x\ty")
                 if "Layer Roughnesses" in analysis_items.values():
                     if result.LayerRoughnesses != None:
                         for i in range(len(result.LayerRoughnesses)):
                             output_txt_file.write("\tLR{}".format(i))
                 if "Layer Thicknesses" in analysis_items.values():
                     if result.LayerThicknesses != None:
                         for i in range(len(result.LayerThicknesses)):
                             output_txt_file.write("\tLayerThickness{}".format(i))
                 if "Measured FFT Intensity" in analysis_items.values():
                     if result.MeasFFTIntensity != None:
                         for i in range(len(result.MeasFFTIntensity)):
                             output_txt_file.write("\tFFTIntensity{}".format(i))
                 if "Measured FFT Thickness" in analysis_items.values():
                     if result.MeasFFTThickness != None:
                         for i in range(len(result.MeasFFTThickness)):
                             output_txt_file.write("\tFFTThickness{}".format(i))
                 output_txt_file.write("\n")


            # Write the file name which includes x and y coordinates in it
            coordinates_string = file[len(map_name)+1:]
            coordinates_string = coordinates_string[:-4]
            for char in "xy":
                coordinates_string = coordinates_string.replace(char, '')
            coordinates_string = coordinates_string.replace('_','\t')
            output_txt_file.write(coordinates_string)

            # Write the items for each file
            if "Layer Roughnesses" in analysis_items.values():
                if result.LayerRoughnesses != None:
                    for i in result.LayerRoughnesses:
                        output_txt_file.write("\t{}".format(i))
            if "Layer Thicknesses" in analysis_items.values():
                if result.LayerThicknesses != None:
                    for i in result.LayerThicknesses:
                        output_txt_file.write("\t{}".format(i))
            if "Measured FFT Intensity" in analysis_items.values():
                if result.MeasFFTIntensity != None:
                    for i in result.MeasFFTIntensity:
                        output_txt_file.write("\t{}".format(i))
            if "Measured FFT Thickness" in analysis_items.values():
                if result.MeasFFTThickness != None:
                    for i in result.MeasFFTThickness:
                        output_txt_file.write("\t{}".format(i))

            # New line
            output_txt_file.write("\n")

        # After everything is written, close the file
        output_txt_file.close()
        self.message1 = "Analysis successfully saved!"
