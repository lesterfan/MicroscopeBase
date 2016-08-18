import pygame
from pygame.locals import *
from pgu import gui
import colors

attribute_items = ["Layer Roughnesses", "Layer Thicknesses", "Measured FFT Intensity", "Measured FFT Thickness"]
display = pygame.display.set_mode((400, 325))
clock = pygame.time.Clock()

def main():
    gui_app = gui.App()
    gui_container = gui.Container(align = -1, valign = -1) 

    gui_container.add(gui.Label("Post Processing Shopping Cart", color = colors.blue), 85, 10)
    
    initial_attributes_list_object = gui.List(width = 180, height = 180)
    for i in range(len(attribute_items)):
        item = attribute_items[i]
        initial_attributes_list_object.add(item, value = i)
    gui_container.add(initial_attributes_list_object, 10, 40)

    cart_items_object = gui.List(width = 180, height = 180)
    gui_container.add(cart_items_object, 210, 40)

    def add_item_to_cart(arg):
        v = initial_attributes_list_object.value
        if v != None:
            index = v
            cart_items_object.add(attribute_items[index], value = index)
            cart_items_object.resize()
            cart_items_object.repaint()
    add_to_cart_button = gui.Button("Add to cart", width = 90)
    add_to_cart_button.connect(gui.CLICK, add_item_to_cart, None)
    gui_container.add(add_to_cart_button, 10, 240)
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