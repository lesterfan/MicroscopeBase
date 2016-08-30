from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply, AsciiAxis
import helper_minion_functions
from msvcrt import getch
import pygame
import time
import printfunctions
import colors
import gameobjects


pygame.init()
pygame.joystick.init()

using_joystick = False


# ---------------------------------------------- Here, I am connecting the microscope with the computer --------------------------------------------------------
FPS = 60
CLOCK = pygame.time.Clock()

DISPLAY_WIDTH = 320                               # The microscope goes from 0 to 640k, so I'll do a factor of 2
DISPLAY_HEIGHT = 384                              # The microscope goes from 0 to 768k, so I'll do a factor of 2
LOCATION_HEIGHT = 50
INSTRUCTION_HEIGHT = 50

MICROSCOPE_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+LOCATION_HEIGHT + INSTRUCTION_HEIGHT))

# Set the title
pygame.display.set_caption("HMNL (tm) 2016: All rights reserved.")

if using_joystick:
    JOYSTICK = pygame.joystick.Joystick(0)
    JOYSTICK.init()

    NUM_BUTTONS = JOYSTICK.get_numbuttons()

# Connecting to the controller port, which is stored in "COM3"

SERIAL = AsciiSerial("COM5")

# Communicate with the microscope base through microscope_base

MICROSCOPE_BASE = AsciiDevice(SERIAL, 1)

unit_change = 1000

# two axes
X_AXIS = AsciiAxis(MICROSCOPE_BASE, 1)
Y_AXIS = AsciiAxis(MICROSCOPE_BASE, 2)

# Microscope man shown on screen
MICROSCOPE_MAN = gameobjects.Enemy(0,0,10,10, colors.white)

# Saved locations shown on screen
DEFAULT_OUT_OF_SCREEN_VALUE = 100000
A_BUTTON_LOC = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.green)                      # The green A button will always be set to home
X_BUTTON_LOC = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.blue)                         # The blue X button will be reconfigurable
Y_BUTTON_LOC = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.yellow)                       # The yellow Y button will be reconfigurable
B_BUTTON_LOC = gameobjects.Enemy(DEFAULT_OUT_OF_SCREEN_VALUE, DEFAULT_OUT_OF_SCREEN_VALUE, 10, 10, colors.red)                          # The red B button will be reconfigurable

dank_meme_on = False

# ---------------------------------------------- End ------------------------------------------------------------------------------------------------------------

def get_absolute_position():

    '''
    Returns a tuple of the absolute location of the device right now
    param : None
    return : (location_x, location_y)
    '''
  
    reply = MICROSCOPE_BASE.send("get pos")
    position_array = reply.data.split()
    x_curr = int(position_array[0])
    y_curr = int(position_array[1])

    return (x_curr, y_curr)

def manual_movement_mode():

    ''' 
    Enters a mode that allows the user to move the base with arrow keys, or with a joystick.
    param : None
    return : None
    '''

    x_change = 0
    y_change = 0
    x_loc = 0
    y_loc = 0
    
    helper_message = ""

    while True:
        
        '''key = ord(getch())
        # if key == 27:   # ESC
        #     return
        # elif key == 72: # UP
        #     x_change = 0
        #     y_change = -unit_change
        # elif key == 75: # LEFT
        #     x_change = unit_change
        #     y_change = 0
        # elif key == 77: # RIGHT
        #     x_change = -unit_change
        #     y_change = 0
        # elif key == 80: # DOWN
        #     x_change = 0
        #     y_change = unit_change
        '''
                
        # -------------------------------------- Using the arrow keys to move ------------------------------------

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            x_change = -unit_change
        if keys[pygame.K_RIGHT]:
            x_change = unit_change
        if keys[pygame.K_DOWN]:
            y_change = unit_change
        if keys[pygame.K_UP]:
            y_change = -unit_change

            
        if keys[pygame.K_a]:
            x_change = -unit_change*100
        if keys[pygame.K_d]:
            x_change = unit_change*100
        if keys[pygame.K_w]:
            y_change = unit_change*100
        if keys[pygame.K_s]:
            y_change = -unit_change*100

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYUP:
                x_change = 0
                y_change = 0

        # -------------------------------------- End Arrow Keys ---------------------------------------------------
        a_button =  0
        x_button =  0
        y_button =  0
        b_button =  0
        rb_button = 0
        start_button = 0
        rt_button = 0
       
        if using_joystick:
            # -------------------------------------- Assign the buttons for the joystick OR on the keyboard -------------------------------------------------
            a_button = JOYSTICK.get_button(0)
            x_button = JOYSTICK.get_button(3)
            y_button = JOYSTICK.get_button(4)
            b_button = JOYSTICK.get_button(1)
            rb_button = JOYSTICK.get_button(7)   
            start_button = JOYSTICK.get_button(11)
            rt_button = JOYSTICK.get_button(9)

        else:
            if keys[pygame.K_h]:
                a_button = 1
            if keys[pygame.K_x]:
                x_button = 1
            if keys[pygame.K_z]:
                y_button = 1
            if keys[pygame.K_c]:
                b_button = 1
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                rb_button = 1 

        # Dank meme
        if rt_button == 1:
            dank_meme_on = True
        # End dank meme

        if start_button == 1:                                                       # Press a to return to a position. Press rb + a to save a position for a
            reply = MICROSCOPE_BASE.home()
            if helper_minion_functions.check_command_succeeded(reply):
                helper_message = "Device homed!"
            else:
                print("device home failed")
                return

        if rb_button == 0 and a_button == 1:                                                       # Press a to return to a position. Press rb + a to save a position for a
            if A_BUTTON_LOC.xstart == DEFAULT_OUT_OF_SCREEN_VALUE:
                helper_message = "No saved value for a!"
            else:
                reply = X_AXIS.move_abs(A_BUTTON_LOC.microscope_x)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                reply = Y_AXIS.move_abs(A_BUTTON_LOC.microscope_y)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                MICROSCOPE_MAN.xstart = A_BUTTON_LOC.xstart
                MICROSCOPE_MAN.ystart = A_BUTTON_LOC.ystart
                helper_message = "Returned to saved x position!"
        
        if rb_button == 0 and x_button == 1:                                    # Press x to return to x position. Press rb + x to save a position for x
            if X_BUTTON_LOC.xstart == DEFAULT_OUT_OF_SCREEN_VALUE:
                helper_message = "No saved value for x!"
            else:
                reply = X_AXIS.move_abs(X_BUTTON_LOC.microscope_x)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                reply = Y_AXIS.move_abs(X_BUTTON_LOC.microscope_y)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                MICROSCOPE_MAN.xstart = X_BUTTON_LOC.xstart
                MICROSCOPE_MAN.ystart = X_BUTTON_LOC.ystart
                helper_message = "Returned to saved x position!"

        if rb_button == 0 and y_button == 1:                                    # Press y to return to y position. Press rb + y to save a position for y
            if Y_BUTTON_LOC.xstart == DEFAULT_OUT_OF_SCREEN_VALUE:
                helper_message = "No saved value for y!"
            else:
                reply = X_AXIS.move_abs(Y_BUTTON_LOC.microscope_x)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                reply = Y_AXIS.move_abs(Y_BUTTON_LOC.microscope_y)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                MICROSCOPE_MAN.xstart = Y_BUTTON_LOC.xstart
                MICROSCOPE_MAN.ystart = Y_BUTTON_LOC.ystart
                helper_message = "Returned to saved y position!"

        if rb_button == 0 and b_button == 1:                                    # Press b to return to b position. Press rb + b to save a position for b
            if B_BUTTON_LOC.xstart == DEFAULT_OUT_OF_SCREEN_VALUE:
                helper_message = "No saved value for b!"
            else:
                reply = X_AXIS.move_abs(B_BUTTON_LOC.microscope_x)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                reply = Y_AXIS.move_abs(B_BUTTON_LOC.microscope_y)
                if not helper_minion_functions.check_command_succeeded(reply):
                    return
                MICROSCOPE_MAN.xstart = B_BUTTON_LOC.xstart
                MICROSCOPE_MAN.ystart = B_BUTTON_LOC.ystart
                helper_message = "Returned to saved b position!"

        if rb_button == 1 and a_button == 1:                                    # Save a location for x by pressing rb + x
            A_BUTTON_LOC.xstart = DISPLAY_WIDTH - int(x_loc/1000) - 10
            if A_BUTTON_LOC.xstart <= 0:
                A_BUTTON_LOC.xstart = 0 
            A_BUTTON_LOC.ystart = int(y_loc/1000)
            A_BUTTON_LOC.microscope_x = x_loc
            A_BUTTON_LOC.microscope_y = y_loc
            helper_message = "x location saved!"                    

        if rb_button == 1 and x_button == 1:                                    # Save a location for x by pressing rb + x
            X_BUTTON_LOC.xstart = DISPLAY_WIDTH - int(x_loc/1000) - 10
            if X_BUTTON_LOC.xstart <= 0:
                X_BUTTON_LOC.xstart = 0 
            X_BUTTON_LOC.ystart = int(y_loc/1000)
            X_BUTTON_LOC.microscope_x = x_loc
            X_BUTTON_LOC.microscope_y = y_loc
            helper_message = "x location saved!"
        
        if rb_button == 1 and y_button == 1:                                    # Save a location for y by pressing rb + y
            Y_BUTTON_LOC.xstart = DISPLAY_WIDTH - int(x_loc/1000) - 10
            if Y_BUTTON_LOC.xstart <= 0:
                Y_BUTTON_LOC.xstart = 0 
            Y_BUTTON_LOC.ystart = int(y_loc/1000)
            Y_BUTTON_LOC.microscope_x = x_loc
            Y_BUTTON_LOC.microscope_y = y_loc
            helper_message = "y location saved!"
            
        if rb_button == 1 and b_button == 1:                                    # Save a location for b by pressing rb + b
            B_BUTTON_LOC.xstart = DISPLAY_WIDTH - int(x_loc/1000) - 10
            if B_BUTTON_LOC.xstart <= 0:
                B_BUTTON_LOC.xstart = 0 
            B_BUTTON_LOC.ystart = int(y_loc/1000)
            B_BUTTON_LOC.microscope_x = x_loc
            B_BUTTON_LOC.microscope_y = y_loc
            helper_message = "b location saved!"

        # -------------------------------------- End button assignments -------------------------------------------------------

        # -------------------------------------- Getting the joystick to move it --------------------------------

        if using_joystick:                                                   
            x_move = JOYSTICK.get_axis(0)                                    # Left trackball to move it slow
            y_move = JOYSTICK.get_axis(1)


            if abs(x_move) >= 0.07:
                x_change += int(x_move*10)
                # x_change = unit_change
            else:
                x_change = 0


            if abs(y_move) >= 0.07:
                y_change += int(y_move*10)
                # y_change = unit_change
            else:
                y_change = 0

            x_move_fast = JOYSTICK.get_axis(2)                               # Right trackball to move it fast
            y_move_fast = JOYSTICK.get_axis(3)

            if abs(x_move_fast) >= 0.07:
                x_change = int(x_move_fast*100000)
                # x_change = unit_change
            else:
                x_change += 0


            if abs(y_move_fast) >= 0.07:
                y_change = int(y_move_fast*100000)
                # y_change = unit_change
            else:
                y_change += 0

        # -------------------------------------- End joystick ----------------------------------------------------


        reply = X_AXIS.move_vel(x_change)
        if not helper_minion_functions.check_command_succeeded(reply):
            return
        reply = Y_AXIS.move_vel(y_change)
        if not helper_minion_functions.check_command_succeeded(reply):
            return
        
        (x_loc, y_loc) = get_absolute_position()
        MICROSCOPE_DISPLAY.fill(colors.black)

        # Drawing in the saved locations

        A_BUTTON_LOC.drawToScreen()
        X_BUTTON_LOC.drawToScreen()
        Y_BUTTON_LOC.drawToScreen()
        B_BUTTON_LOC.drawToScreen()

        # Configuring the location of microscope man

        MICROSCOPE_MAN.xstart = int(x_loc/2000)
        if MICROSCOPE_MAN.xstart <= 0:
            MICROSCOPE_MAN.xstart = 0 
        MICROSCOPE_MAN.ystart = int(y_loc/2000)
        MICROSCOPE_MAN.drawToScreen()

        pygame.draw.rect(MICROSCOPE_DISPLAY, colors.white, [0, 389, 320, 100])
        pygame.draw.rect(MICROSCOPE_DISPLAY, colors.red, [0, 389, 320, 10])

        # print("Location : ("+str(x_loc)+","+str(y_loc)+")")
        printfunctions.message_to_screen("Location : ("+str(x_loc)+","+str(y_loc)+")",colors.black, y_displace = 180, size = 'medium')
        printfunctions.message_to_screen(helper_message,colors.black, y_displace = 200)
        printfunctions.message_to_screen("RB + X,Y,B to save a position. Press X,Y,B to return to that", colors.black, y_displace = 215)
        printfunctions.message_to_screen("position. A to home.", colors.black, y_displace = 225)
        pygame.display.update()
        CLOCK.tick(FPS)
        
       

def main():
    '''
    microscope_base.poll_until_idle()

     Home the microscope
     reply = MICROSCOPE_BASE.home()
     if helper_minion_functions.check_command_succeeded(reply):
         print ("Device Homed!")
     else:
         print ("Device home failed!")
         return
    
     reply = X_AXIS.move_vel(10)    # Move rel 6.4 microsteps = 1um
     if helper_minion_functions.check_command_succeeded(reply):
         print ("Device moved")
     else:
         print ("Device move failed!")
         return
    
     Make the device has finished its previous move before sending the
     next command. Note that this is unnecessary in this case as the
     AsciiDevice.home command is blocking, but this would be required if
     the AsciiDevice.send command is used to trigger movement.
    microscope_base.poll_until_idle()


     print x_curr, y_curr
     '''
    print "What's good in the hood"

    manual_movement_mode()

    # Cleaning things up
    SERIAL.close()
    
    print ("Microns!")

main()