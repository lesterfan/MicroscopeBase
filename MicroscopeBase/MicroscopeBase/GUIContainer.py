import pygame
from pygame.locals import *
from pgu import gui
import colors
import os

from FinishedMap import FinishedMap

class GUIContainer(gui.Container):
    """description of class"""
    Interface = None
    Microscope_Base = None

    joystick_selection = None
    update_joystick_button = None
    update_joystick_button_clicked = False

    fmspe_dir_input = None
    fmspe_browse_button = None

    xml_dir_input = None
    xml_browse_button = None
    
    image_dir_input = None
    image_browse_button = None

    map_name_input = None

    unit_selection = None
    num_pts_x_input = None
    distance_bw_pts_x_input = None
    num_pts_y_input = None
    distance_bw_pts_y_input = None

    take_measurement_button = None
    # take_measurement_button_clicked = False
    start_or_pause_button = None
    # start_or_pause_button_clicked = False
    stop_button = None
    # stop_button_clicked = False

    started_map = False


    def __init__(self, interface = None , **params):
        gui.Container.__init__(self, **params)

        self.Interface = interface
        self.add(gui.Label("Microscope Analyzer - HMNL (tm) 2016", color = colors.blue), 95, 5)
        
        # Select joystick GUI
        self.add(gui.Label("Select joystick"), 7, 32)
        self.joystick_selection = gui.Select()
        # self.joystick_selection.add("None",'None')
        self.joystick_selection.add("Shenzhen",'Shenzhen')
        self.joystick_selection.add("The unworking backup", "The unworking backup")
        self.joystick_selection.add("Xbox >>>>> Playstation", "Xbox >>>>> Playstation")
        self.add(self.joystick_selection, 150, 30)
        
        # Update joystick button
        def UpdateJoystickButtonCallBack():
            if self.joystick_selection.value == "Shenzhen" or self.joystick_selection.value == "Xbox >>>>> Playstation":
                self.Interface.initialize_joystick()
            else:
                self.Interface.initialize_joystick(self, a_button_num = 0, x_button_num = 2, y_button_num = 3,
                                    b_button_num = 1, rb_button_num = 5, start_button_num = 7, 
                                    lx_axis = 0, ly_axis = 1, trigger_axis = 2, rx_axis = 3, ry_axis = 4, 
                                    rt_button_num = None, lt_button_num = None)
        self.update_joystick_button = gui.Button("Update JS")
        self.update_joystick_button.connect(gui.CLICK, UpdateJoystickButtonCallBack)
        self.add(self.update_joystick_button, 400, 32)

        # Input FMSPE directory / internal callback functions to handle buttons being clicked
        self.add(gui.Label("FMPSE directory", color = colors.black), 7, 62)
        def handle_fmspe_file_browser_closed(dlg):
            if dlg.value : self.fmspe_dir_input.value = dlg.value
        def open_fmspe_file_browser(arg):
            d = gui.FileDialog(path = "C:\\Users\\HMNL\\Documents\\Test\\")
            d.connect(gui.CHANGE, handle_fmspe_file_browser_closed, d)
            d.open()
        self.fmspe_dir_input = gui.Input(size = 25)
        self.add(self.fmspe_dir_input, 150, 60)
        self.fmspe_browse_button = gui.Button("Browse...")
        self.fmspe_browse_button.connect(gui.CLICK, open_fmspe_file_browser, None)
        self.add(self.fmspe_browse_button, 400, 62)

        # Input XML directory / internal callback functions to handle buttons being clicked
        self.add(gui.Label("XML directory", color = colors.black), 7, 92)
        def handle_xml_file_browser_closed(dlg):
            if dlg.value : self.xml_dir_input.value = dlg.value
        def open_xml_file_browser(arg):
            d = gui.FileDialog(path = "C:\\Users\\HMNL\\Documents\\Test\\")
            d.connect(gui.CHANGE, handle_xml_file_browser_closed, d)
            d.open()
        self.xml_dir_input = gui.Input(size = 25)
        self.add(self.xml_dir_input, 150, 90)
        self.xml_browse_button = gui.Button("Browse...")
        self.xml_browse_button.connect(gui.CLICK, open_xml_file_browser, None)
        self.add(self.xml_browse_button, 400, 92)

        # Input image directory / internal callback functions to handle buttons being clicked
        self.add(gui.Label("Image directory", color = colors.black), 7, 122)
        def handle_image_file_browser_closed(dlg):
            if dlg.value : self.image_dir_input.value = dlg.value
        def open_image_file_browser(arg):
            d = gui.FileDialog(path = "C:\\Users\\HMNL\\Documents\\Test\\")
            d.connect(gui.CHANGE, handle_image_file_browser_closed, d)
            d.open()
        self.image_dir_input = gui.Input(size = 25)
        self.add(self.image_dir_input, 150, 120)
        self.image_browse_button = gui.Button("Browse...")
        self.image_browse_button.connect(gui.CLICK, open_image_file_browser, None)
        self.add(self.image_browse_button, 400, 122)

        # Get the name that the user wants the map to be called
        self.add(gui.Label("Map name"), 7, 152)
        self.map_name_input = gui.Input(size = 25)
        self.add(self.map_name_input, 107, 150)

        # Get the units of measurement
        self.add(gui.Label("Units"), 365, 152)
        self.unit_selection = gui.Select()
        self.unit_selection.add("um",'um')
        self.unit_selection.add("mm",'mm')
        self.add(self.unit_selection, 425, 150)

        # Inputs for the mapping function
        self.add(gui.Label("Number Points X"), 7, 182)
        self.num_pts_x_input = gui.Input(size = 5)
        self.add(self.num_pts_x_input, 155, 180)
        
        self.add(gui.Label("Distance b/w Points X"), 237, 182)
        self.distance_bw_pts_x_input = gui.Input(size = 5)
        self.add(self.distance_bw_pts_x_input, 425, 180)
        
        self.add(gui.Label("Number Points Y"), 7, 212)
        self.num_pts_y_input = gui.Input(size = 5)
        self.add(self.num_pts_y_input, 155, 210)
        
        self.add(gui.Label("Distance b/w Points Y"), 237, 212)
        self.distance_bw_pts_y_input = gui.Input(size = 5)
        self.add(self.distance_bw_pts_y_input, 425, 210)

        # Measure, Start/Pause, Stop buttons
        def MeasureOnceButtonCallback():
            self.Interface.message1 = "Taking measurement!"
            self.Interface.take_measurement()
        self.take_measurement_button = gui.Button("Measure once")
        self.take_measurement_button.connect(gui.CLICK, MeasureOnceButtonCallback)
        self.add(self.take_measurement_button, 17, 242)

        def StartOrPauseButtonCallback():
            print "Map started!"
            if not self.started_map :       # If it's the first time, then start taking the map
                self.started_map = True
                try:
                    self.Interface.take_map(self.map_name_input.value, int(self.num_pts_x_input.value),
                                            int(self.distance_bw_pts_x_input.value), int(self.num_pts_y_input.value),
                                            int(self.distance_bw_pts_y_input.value), self.unit_selection.value, 
                                            self.Microscope_Base)
                    self.started_map = False
                except Exception:
                    print "Error with taking map!"

            else :                          # If a map is already in progress, pause it
                self.Interface.pause_button_pressed = True

        self.start_or_pause_button = gui.Button("Start / Pause Map")
        self.start_or_pause_button.connect(gui.CLICK, StartOrPauseButtonCallback)
        self.add(self.start_or_pause_button, 190, 242)

        def StopButtonCallback():
            self.Interface.stop_button_pressed = True
            
        self.stop_button = gui.Button("Stop map")
        self.stop_button.connect(gui.CLICK, StopButtonCallback)
        self.add(self.stop_button, 390, 242)




        # ----------------------------------------------- Post Processing GUI Components -------------------------------------------------------------------------------

        xalign = 830                    # Alignment between standalone program and the final program
        attribute_items = ["Layer Roughnesses", "Layer Thicknesses", "Measured FFT Intensity", "Measured FFT Thickness"]           # Attributes that are available to write to .txt file
        cart_items = {}

        self.add(gui.Label("Post Processing Shopping Cart", color = colors.blue), xalign + 85, 10)
        
        # Attributes list from which the user can pick out items
        initial_attributes_list_object = gui.List(width = 180, height = 140)
        for i in range(len(attribute_items)):
            item = attribute_items[i]
            initial_attributes_list_object.add(item, value = i)
        self.add(initial_attributes_list_object, xalign + 10, 40)

        # List of items that the user selected into their carts
        cart_items_object = gui.List(width = 180, height = 140)
        self.add(cart_items_object, xalign + 210, 40)

        # Functions to add/remove items from cart 
        def add_item_to_cart(arg):
            v = initial_attributes_list_object.value
            if v != None and v not in cart_items:
                cart_items[v] = attribute_items[v]
                index = v
                cart_items_object.add(attribute_items[index], value = index)
                cart_items_object.resize()
                cart_items_object.repaint()
                
        def remove_item_from_cart(arg):
            v = cart_items_object.value
            if v != None:
                cart_items.pop(v)
                cart_items_object.remove(v)
                cart_items_object.resize()
                cart_items_object.repaint()
                cart_items_object.value = None

        # Performs analysis and saves it as a .txt file in the out directory that the user specifies
        def check_out(arg):
            self.Interface.PostProcessAndSave(xml_directory_post_processing.value, text_dir_input.value, post_map_name_input.value, cart_items)

        # Cart button GUI objects... the functions are defined above
        add_to_cart_button = gui.Button("Add to cart", width = 90)
        add_to_cart_button.connect(gui.CLICK, add_item_to_cart, None)
        self.add(add_to_cart_button, xalign + 10, 190)

        remove_from_cart_button = gui.Button("Remove from cart", width = 90)
        remove_from_cart_button.connect(gui.CLICK, remove_item_from_cart, None)
        self.add(remove_from_cart_button, xalign + 125, 190)

        save_analysis_button = gui.Button("Checkout", width = 85)
        save_analysis_button.connect(gui.CLICK, check_out, None)
        self.add(save_analysis_button, xalign + 290, 190)
        
        # The name of the map that we should be looking for
        self.add(gui.Label("Map name"), xalign + 7, 222)
        post_map_name_input = gui.Input(size = 28)
        post_map_name_input.value = "Columbus"
        self.add(post_map_name_input, xalign + 125, 220) 

        # Post processing XML directory input
        def handle_xml_post_file_browser_closed(dlg):
            if dlg.value : xml_directory_post_processing.value = dlg.value
        def open_xml_post_file_browser(arg):
            d = gui.FileDialog(path = "C:\\Users\\HMNL\\Documents\\Test\\")
            d.connect(gui.CHANGE, handle_xml_post_file_browser_closed, d)
            d.open()
        xml_directory_post_processing = gui.Input(size = 19)
        xml_directory_post_processing.value = "C:\\Users\\HMNL\\Documents\\Test\\XML\\"
        self.add(gui.Label("XML Directory"),    xalign + 7, 252)
        self.add(xml_directory_post_processing, xalign + 125, 250)
        post_browse_button = gui.Button("Browse", width = 50)
        self.add(post_browse_button, xalign + 315, 252)
        post_browse_button.connect(gui.CLICK, open_xml_post_file_browser, None)

        # Output file directory
        def handle_text_browser_closed(dlg):
            if dlg.value : text_dir_input.value = dlg.value
        def open_text_file_browser(arg):
            d = gui.FileDialog(path = "C:\\Users\\HMNL\\Documents\\Test\\")
            d.connect(gui.CHANGE, handle_text_browser_closed, d)
            d.open()
        text_dir_input = gui.Input(size = 19)
        text_dir_input.value = "C:\\Users\\HMNL\\Documents\\Test\\AnalysisFiles\\"
        self.add(gui.Label("Out Directory"), xalign + 7, 282)
        self.add(text_dir_input,             xalign + 125, 280)
        text_dir_browse_button = gui.Button("Browse", width = 50)
        self.add(text_dir_browse_button, xalign + 315, 282)
        text_dir_browse_button.connect(gui.CLICK, open_text_file_browser, None)
        

        # ------------------------------------------------------- View / Delete Map History -----------------------------------------------------------------
            
        yalign = 325                   # Alignment between standalone program and the final program
        cart_items = {}

        self.add(gui.Label("Map History", color = colors.blue), 575, yalign)
        lines = [line.rstrip('\n') for line in open("History/map_history.txt")]

        # Attributes list from which the user can pick out items
        maps_in_history_list = gui.List(width = 200, height = 270)
        for i in range(len(lines)):
            vals_array = lines[i].split(" ")
            new_map_info = FinishedMap(vals_array[0], vals_array[1], vals_array[2], vals_array[3], vals_array[4],
                                       vals_array[5], vals_array[6], vals_array[7], vals_array[8], vals_array[9], vals_array[10])
            self.Interface.map_history.append(new_map_info)

            maps_in_history_list.add(new_map_info.map_name, value = i)

        self.add(maps_in_history_list, 300, yalign + 30)

        MapNameLabel                    = gui.Input(size = 40)
        FMSPEDirLabel                   = gui.Input(size = 40)
        XMLDirLabel                     = gui.Input(size = 40)
        ImageDirLabel                   = gui.Input(size = 40)
        NumMeasurementsXLabel           = gui.Input(size = 40)
        DistanceMeasurementsXLabel      = gui.Input(size = 40)
        NumMeasurementsYLabel           = gui.Input(size = 40)
        DistanceMeasurementsYLabel      = gui.Input(size = 40)
        DateTakenLabel                  = gui.Input(size = 40)
        TimeTakenLabel                  = gui.Input(size = 40)
        UnitsLabel                      = gui.Input(size = 40)
       
        self.add(gui.Label("Map name : "                   ), 525, yalign + 30 )
        self.add(gui.Label("FMSPE Dir : "                  ), 525, yalign + 55 )
        self.add(gui.Label("XML Dir : "                    ), 525, yalign + 80 )
        self.add(gui.Label("Image Dir : "                  ), 525, yalign + 105)
        self.add(gui.Label("# Measurements x : "           ), 525, yalign + 130)
        self.add(gui.Label("Distance b/w x meas. : "),        525, yalign + 155)
        self.add(gui.Label("# Measurements y : "           ), 525, yalign + 180)
        self.add(gui.Label("Distance b/w y meas.: "),         525, yalign + 205)
        self.add(gui.Label("Date taken : "                 ), 525, yalign + 230)
        self.add(gui.Label("Time taken : "                 ), 525, yalign + 255)
        self.add(gui.Label("Units: "                 ),       525, yalign + 280)
                 
        self.add(MapNameLabel              , 720, yalign + 30 )
        self.add(FMSPEDirLabel             , 720, yalign + 55 )
        self.add(XMLDirLabel               , 720, yalign + 80 )
        self.add(ImageDirLabel             , 720, yalign + 105)
        self.add(NumMeasurementsXLabel     , 720, yalign + 130)
        self.add(DistanceMeasurementsXLabel, 720, yalign + 155)
        self.add(NumMeasurementsYLabel     , 720, yalign + 180)
        self.add(DistanceMeasurementsYLabel, 720, yalign + 205)
        self.add(DateTakenLabel            , 720, yalign + 230)
        self.add(TimeTakenLabel            , 720, yalign + 255)
        self.add(UnitsLabel                , 720, yalign + 280)

        def show_info():
            v = maps_in_history_list.value
            if v == None:
                return
            try:
                MapNameLabel.value = "{}".format(self.Interface.map_history[v].map_name)
                FMSPEDirLabel.value = "{}".format(self.Interface.map_history[v].fmspedir)
                XMLDirLabel.value= "{}".format(self.Interface.map_history[v].xmldir  )
                ImageDirLabel.value= "{}".format(self.Interface.map_history[v].imagedir)
                NumMeasurementsXLabel.value= "{}".format(self.Interface.map_history[v].numx    )
                DistanceMeasurementsXLabel.value= "{}".format(self.Interface.map_history[v].distbwx )
                NumMeasurementsYLabel.value= "{}".format(self.Interface.map_history[v].numy    )
                DistanceMeasurementsYLabel.value= "{}".format(self.Interface.map_history[v].distbwy )
                DateTakenLabel.value= "{}".format(self.Interface.map_history[v].date    )
                TimeTakenLabel.value= "{}".format(self.Interface.map_history[v].time    )
                UnitsLabel.value= "{}".format(self.Interface.map_history[v].units    )
            except BaseException:
                pass


            # print v
            # print MapNameLabel.value


        maps_in_history_list.connect(gui.CLICK, show_info)



        # Implementing delete
        def delete():
            v = maps_in_history_list.value
            if v == None:
                return

            # Get directories and map name
            map_name = self.Interface.map_history[v].map_name

            fmspe_dir = self.Interface.map_history[v].fmspedir
            xml_dir   = self.Interface.map_history[v].xmldir  
            image_dir = self.Interface.map_history[v].imagedir

            # Gather all relevant files
            try:
                fmspe_files = [filename for filename in os.listdir(fmspe_dir) if filename.startswith(map_name) and filename.endswith(".fmspe")]
                xml_files   = [filename for filename in os.listdir(xml_dir) if filename.startswith(map_name) and filename.endswith(".xml")]
                image_files = [filename for filename in os.listdir(image_dir) if filename.startswith(map_name) and filename.endswith(".bmp")]
            except WindowsError:
                fmspe_files = []
                xml_files   = []
                image_files = []


            # Delete all these relevant files
            for file in fmspe_files:
                try:
                    os.remove(fmspe_dir + file)
                except WindowsError:
                    print "Couldn't find {}!".format(file)
            for file in xml_files:
                try:
                    os.remove(xml_dir + file)
                except WindowsError:
                    print "Couldn't find {}!".format(file)
            for file in image_files:
                try:
                    os.remove(image_dir + file)
                except WindowsError:
                    print "Couldn't find {}!".format(file)

            # Remove the map from the text file
            old_lines = [line.rstrip('\n') for line in open("History/map_history.txt")]
            
            with open("History/map_history.txt", "w") as f:
                map_name       = self.Interface.map_history[v].map_name 
                fmspe_dir      = self.Interface.map_history[v].fmspedir
                xml_dir        = self.Interface.map_history[v].xmldir  
                image_dir      = self.Interface.map_history[v].imagedir
                num_pts_x      = self.Interface.map_history[v].numx
                dist_bw_x      = self.Interface.map_history[v].distbwx
                num_pts_y      = self.Interface.map_history[v].numy
                dist_bw_y      = self.Interface.map_history[v].distbwy
                date           = self.Interface.map_history[v].date   
                time           = self.Interface.map_history[v].time   
                units          = self.Interface.map_history[v].units    
            
                for line in old_lines:
                    # print line
                    compare_line = "{} {} {} {} {} {} {} {} {} {} {}".format(map_name, fmspe_dir, 
                                                                         xml_dir, image_dir, 
                                                                         num_pts_x, dist_bw_x, num_pts_y, dist_bw_y, 
                                                                         date, time, units)
                    # print compare_line
                    if line != compare_line:
                        f.write("{}\n".format(line))
            
            # The lines present in the file afterwards... Now we refill the list with these values
            new_lines = [line.rstrip('\n') for line in open("History/map_history.txt")]

            # Reset map history
            self.Interface.map_history = []
            maps_in_history_list.clear()

            
            for i in range(len(new_lines)):
                vals_array = new_lines[i].split(" ")
                new_map_info = FinishedMap(vals_array[0], vals_array[1], vals_array[2], vals_array[3], vals_array[4],
                                           vals_array[5], vals_array[6], vals_array[7], vals_array[8], vals_array[9], vals_array[10])
                self.Interface.map_history.append(new_map_info)
                
                maps_in_history_list.add(new_map_info.map_name, value = i)


        delete_button = gui.Button("Delete Map", width = 50)
        self.add(delete_button, 1110, yalign + 30)
        delete_button.connect(gui.CLICK, delete)


        # -------------- UPDATE THE LIST -----------------------------------
        def update_list():
            new_lines = [line.rstrip('\n') for line in open("History/map_history.txt")]

            # Reset map history
            self.Interface.map_history = []
            maps_in_history_list.clear()

            for i in range(len(new_lines)):
                vals_array = new_lines[i].split(" ")
                new_map_info = FinishedMap(vals_array[0], vals_array[1], vals_array[2], vals_array[3], vals_array[4],
                                           vals_array[5], vals_array[6], vals_array[7], vals_array[8], vals_array[9], vals_array[10])
                self.Interface.map_history.append(new_map_info)
                
                maps_in_history_list.add(new_map_info.map_name, value = i)


        update_button = gui.Button("Update List", width = 50)
        self.add(update_button, 1110, yalign + 65)
        update_button.connect(gui.CLICK, update_list)

        # 
        # # List of items that the user selected into their carts
        # cart_items_object = gui.List(width = 180, height = 140)
        # self.add(cart_items_object, xalign + 210, 40)
        # 
        # # Functions to add/remove items from cart 
        # def add_item_to_cart(arg):
        #     v = initial_attributes_list_object.value
        #     if v != None and v not in cart_items:
        #         cart_items[v] = attribute_items[v]
        #         index = v
        #         cart_items_object.add(attribute_items[index], value = index)
        #         cart_items_object.resize()
        #         cart_items_object.repaint()
        #         
        # def remove_item_from_cart(arg):
        #     v = cart_items_object.value
        #     if v != None:
        #         cart_items.pop(v)
        #         cart_items_object.remove(v)
        #         cart_items_object.resize()
        #         cart_items_object.repaint()
        #         cart_items_object.value = None











        # ------------------------------------------------------- Fun -------------------------------------------------------

        # Change theme button
        def change_theme(arg):
            self.Interface.set_theme()
        self.change_theme_button = gui.Button("New Theme")
        self.change_theme_button.connect(gui.CLICK, change_theme, None)
        self.add(self.change_theme_button, 380, 297)




    def set_default_values(self):
        self.joystick_selection.value = "Shenzhen"

        self.fmspe_dir_input.value = "C:\\Users\\HMNL\\Documents\\Test\\FMSPE\\"
        self.xml_dir_input.value = "C:\\Users\\HMNL\\Documents\\Test\\XML\\"
        self.image_dir_input.value = "C:\\Users\\HMNL\\Documents\\Test\\Images\\"

        self.map_name_input.value = "Columbus"
        self.unit_selection.value = "um"

        self.num_pts_x_input.value = '5'
        self.num_pts_y_input.value = '5'
        self.distance_bw_pts_x_input.value = '5'
        self.distance_bw_pts_y_input.value = '5'

    def LTButtonCallback(self):
        print "Map started!"
        if not self.started_map :       # If it's the first time, then start taking the map
            self.started_map = True
            try:
                self.Interface.take_map(self.map_name_input.value, int(self.num_pts_x_input.value),
                                        int(self.distance_bw_pts_x_input.value), int(self.num_pts_y_input.value),
                                        int(self.distance_bw_pts_y_input.value), self.unit_selection.value, 
                                        self.Microscope_Base)
                self.started_map = False
            except SystemError:
                print "Error with taking map!"
        else :                          # If a map is already in progress, pause it
            self.Interface.pause_button_pressed = True


# def main():
#     pygame.init()
#     game_display = pygame.display.set_mode((500,325))
#     gui_app = gui.App()
#     gui_container = GUIContainer(align = -1, valign = -1)
#     gui_container.set_default_values()
#     gui_app.init(gui_container)
# 
#     clock = pygame.time.Clock()
#     
#     while True:
#         for event in pygame.event.get():
#             gui_app.event(event)
#             
#         # print gui_container.joystick_selection.value
#         # if gui_container.take_measurement_button.pcls == "down":
#         #     print "Take measurement button clicked!"
# 
#         game_display.fill(colors.white)
#         gui_app.paint()
#         gui_app.update()
# 
# 
# 
#         pygame.display.update()
#         clock.tick(60)
# main()