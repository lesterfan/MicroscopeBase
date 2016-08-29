import pygame
from pygame.locals import *
from pgu import gui
import colors
import dotnet.seamless
dotnet.add_assemblies('C:\\Users\\Huafeng\\Desktop\\VGitHub\\MicroscopeBase\\MicroscopeBase\\MicroscopeBase')
dotnet.load_assembly('MicroscopeAnalyzerLibrary')
import MicroscopeAnalyzerLibrary



attribute_items = ["Layer Roughnesses", "Layer Thicknesses", "Measured FFT Intensity", "Measured FFT Thickness"]
cart_items = {}
display = pygame.display.set_mode((400, 325))
clock = pygame.time.Clock()

def main():
    gui_app = gui.App()
    gui_container = gui.Container(align = -1, valign = -1) 

    gui_container.add(gui.Label("Post Processing Shopping Cart", color = colors.blue), 85, 10)
    
    initial_attributes_list_object = gui.List(width = 180, height = 140)
    for i in range(len(attribute_items)):
        item = attribute_items[i]
        initial_attributes_list_object.add(item, value = i)
    gui_container.add(initial_attributes_list_object, 10, 40)

    cart_items_object = gui.List(width = 180, height = 140)
    gui_container.add(cart_items_object, 210, 40)

    def add_item_to_cart(arg):
        v = initial_attributes_list_object.value
        print v
        if v != None and v not in cart_items:
            cart_items[v] = v
            index = v
            cart_items_object.add(attribute_items[index], value = index)
            cart_items_object.resize()
            cart_items_object.repaint()
            
    def remove_item_from_cart(arg):
        v = cart_items_object.value
        print v
        if v != None:
            cart_items.pop(v)
            cart_items_object.remove(v)
            cart_items_object.resize()
            cart_items_object.repaint()
            cart_items_object.value = None

    def check_out(arg):
        print "Insufficient funding! Please apply to more grants!"

    add_to_cart_button = gui.Button("Add to cart", width = 90)
    add_to_cart_button.connect(gui.CLICK, add_item_to_cart, None)
    gui_container.add(add_to_cart_button, 10, 190)

    remove_from_cart_button = gui.Button("Remove from cart", width = 90)
    remove_from_cart_button.connect(gui.CLICK, remove_item_from_cart, None)
    gui_container.add(remove_from_cart_button, 125, 190)

    save_analysis_button = gui.Button("Checkout", width = 85)
    save_analysis_button.connect(gui.CLICK, check_out, None)
    gui_container.add(save_analysis_button, 290, 190)
    
    gui_container.add(gui.Label("Map name"), 7, 222)
    post_map_name_input = gui.Input(size = 28)
    post_map_name_input.value = "Columbus"
    gui_container.add(post_map_name_input, 125, 220) 

    def handle_xml_post_file_browser_closed(dlg):
        if dlg.value : xml_directory_post_processing.value = dlg.value
    def open_xml_post_file_browser(arg):
        d = gui.FileDialog(path = "C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\")
        d.connect(gui.CHANGE, handle_xml_post_file_browser_closed, d)
        d.open()
    xml_directory_post_processing = gui.Input(size = 19)
    xml_directory_post_processing.value = "C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\xmlfiles\\"
    gui_container.add(gui.Label("XML Directory"), 7, 252)
    gui_container.add(xml_directory_post_processing, 125, 250)
    post_browse_button = gui.Button("Browse", width = 50)
    gui_container.add(post_browse_button, 315, 252)
    post_browse_button.connect(gui.CLICK, open_xml_post_file_browser, None)

    def handle_text_browser_closed(dlg):
        if dlg.value : text_dir_input.value = dlg.value
    def open_text_file_browser(arg):
        d = gui.FileDialog(value = "C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\AnalysisFiles\\")
        d.connect(gui.CHANGE, handle_text_browser_closed, d)
        d.open()
    text_dir_input = gui.Input(size = 19)
    text_dir_input.value = "C:\\Users\\Huafeng\\Desktop\\TestXMLFiles\\AnalysisFiles\\"
    gui_container.add(gui.Label("Out Directory"), 7, 282)
    gui_container.add(text_dir_input, 125, 280)
    text_dir_browse_button = gui.Button("Browse", width = 50)
    gui_container.add(text_dir_browse_button, 315, 282)
    text_dir_browse_button.connect(gui.CLICK, open_text_file_browser, None)

    gui_app.init(gui_container)

    while True:
        display.fill(colors.white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            gui_app.event(event) 

        # print initial_attributes_list_object.value
        gui_app.paint()
        gui_app.update()
        pygame.display.update()
        clock.tick(60)

main()