import pygame
from pygame.locals import *
from pgu import gui
import colors

class GUIContainer(gui.Container):
    """description of class"""

    joystick_selection = None
    update_joystick_button = None

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
    start_or_pause_button = None
    stop_button = None

    def __init__(self, **params):
        gui.Container.__init__(self, **params)

        self.add(gui.Label("Microscope Analyzer - HMNL (c) 2016", color = colors.blue), 95, 5)
        
        # Select joystick GUI
        self.add(gui.Label("Select joystick"), 7, 32)
        self.joystick_selection = gui.Select()
        self.joystick_selection.add("None",'None')
        self.joystick_selection.add("Shenzhen",'Shenzhen')
        self.joystick_selection.add("The unworking backup", "The unworking backup")
        self.joystick_selection.add("Xbox >>>>> Playstation", "Xbox >>>>> Playstation")
        self.add(self.joystick_selection, 150, 30)
        
        # Update joystick button
        self.update_joystick_button = gui.Button("Update JS")
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
        self.take_measurement_button = gui.Button("Measure once")
        self.add(self.take_measurement_button, 17, 242)

        self.start_or_pause_button = gui.Button("Start / Pause Map")
        self.add(self.start_or_pause_button, 190, 242)

        self.stop_button = gui.Button("Stop map")
        self.add(self.stop_button, 390, 242)


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

# def main():
#     pygame.init()
#     game_display = pygame.display.set_mode((500,325))
#     gui_app = gui.App()
#     gui_container = GUIContainer(align = -1, valign = -1)
#     gui_app.init(gui_container)
# 
#     clock = pygame.time.Clock()
#     
#     while True:
#         for event in pygame.event.get():
#             gui_app.event(event)
# 
#         game_display.fill(colors.white)
#         gui_app.paint()
#         gui_app.update()
# 
#         pygame.display.update()
#         clock.tick(60)
# main()