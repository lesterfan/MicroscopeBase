import pygame
import utility
import colors
import gameobjects

pygame.init()
pygame.joystick.init()

display_width = 800
display_height = 600
FPS = 60
MICROSCOPE_DISPLAY = pygame.display.set_mode((display_width, display_height))
CLOCK = pygame.time.Clock()
JOYSTICK = pygame.joystick.Joystick(0)
JOYSTICK.init()
#TEST_MAN = gameobjects.Catapault(display_width/2, display_height/2, 10, 10, 0)

def main():
    print("hello, world!")

    while True:
        pygame.display.update()
        CLOCK.tick(FPS)
       
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            MICROSCOPE_DISPLAY.fill(colors.black)
            utility.message_to_screen("LEFT", colors.white)
        if keys[pygame.K_RIGHT]:
            MICROSCOPE_DISPLAY.fill(colors.black)
            utility.message_to_screen("RIGHT",colors.white)
        if keys[pygame.K_DOWN]:
            MICROSCOPE_DISPLAY.fill(colors.black)
            utility.message_to_screen("DOWN", colors.white)
        if keys[pygame.K_UP]:
            MICROSCOPE_DISPLAY.fill(colors.black)
            utility.message_to_screen("UP",   colors.white)
        
            
        #a_button = JOYSTICK.get_button(0)
        #x_button = JOYSTICK.get_button(2)
        #y_button = JOYSTICK.get_button(3)
        #b_button = JOYSTICK.get_button(1)
        #rb_button = JOYSTICK.get_button(5) 
        #list_buttons = [a_button,x_button,y_button,b_button,rb_button]
        #
        #print ("Testing buttons!")
        #for button in list_buttons:
        #    print(button)
                


        for event in pygame.event.get():
            # if event.type == pygame.JOYAXISMOTION:
            #     print("Axis",event.axis,"MOTION")
                #print("Position : (",JOYSTICK.get_axis(0),JOYSTICK.get_axis(1),JOYSTICK.get_axis(2),JOYSTICK.get_axis(3),")")

            if event.type == pygame.JOYAXISMOTION:
               if event.axis == 2 or event.axis == 3:
                   print("yeeee")
                   #print("Position : (",JOYSTICK.get_axis(0),JOYSTICK.get_axis(1),")")
                   # TEST_MAN.xstart += JOYSTICK.get_axis(0)
                   # TEST_MAN.ystart += JOYSTICK.get_axis(1)
                   pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYUP:
                pass
                # x_change = 0
                # y_change = 0

        x_move = JOYSTICK.get_axis(0)
        y_move = JOYSTICK.get_axis(1)
        #print (x_move, y_move)
        

        #if abs(x_move) >= 0.1:
        #    TEST_MAN.xstart += x_move*5
        #if abs(y_move) >= 0.1:
        #    TEST_MAN.ystart += y_move*5


        # Testing buttons
        buttons = JOYSTICK.get_numbuttons()
        i = 8
        button = JOYSTICK.get_button(i)
        print("Button {} value {}".format(i,button))

        MICROSCOPE_DISPLAY.fill(colors.black)
        #TEST_MAN.drawToScreen()


main()
pygame.joystick.quit()
pygame.quit()