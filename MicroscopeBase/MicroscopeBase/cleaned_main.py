import MicroscopeBase
import UserInterface
import pygame

def main():
    Microscope_Base = MicroscopeBase.MicroscopeBase("COM5")
    Interface = UserInterface.UserInterface()
    Interface.initialize_joystick()


    unit_change = 1000                           # Each unit of change
    x = 0                                        # Current x position
    y = 0                                        # Current y position
    x_change = 0                                 # Current change in x
    y_change = 0                                 # Current change in y

    # Forever while loop
    while True:
        Interface.check_keyboard_keys()          # Fill Interface.keys with keyboard inputs

        # ------------------------- CONFIGURING SAVE/LOAD BUTTONS -------------------------

        # If button == 1, then it is clicked
        a_button       =   0
        x_button       =   0
        y_button       =   0
        b_button       =   0
        rb_button      =   0
        start_button   =   0
        rt_button      =   0

        # If joystick on, assign the appropriate buttons. If not, assign keyboard ones
        if Interface.using_joystick:
            Interface.check_joystick_button()
            a_button       = Interface.a_button    
            x_button       = Interface.x_button    
            y_button       = Interface.y_button    
            b_button       = Interface.b_button    
            rb_button      = Interface.rb_button   
            start_button   = Interface.start_button
            rt_button      = Interface.rt_button   
        else:
            if Interface.keys[pygame.K_h]:
                start_button = 1
            if Interface.keys[pygame.K_v]:
                a_button = 1
            if Interface.keys[pygame.K_x]:
                x_button = 1
            if Interface.keys[pygame.K_z]:
                y_button = 1
            if Interface.keys[pygame.K_c]:
                b_button = 1
            if Interface.keys[pygame.K_LSHIFT] or Interface.keys[pygame.K_RSHIFT]:
                rb_button = 1 

        # Checking if each button is pressed. If so, do appropriate actions.
        if start_button == 1:                                              # Start button to home device
            Microscope_Base.home_device()

        if rb_button == 1 and a_button == 1:                               # Save functions
            Interface.save_position_to_button('a',Microscope_Base)

        if rb_button == 1 and x_button == 1:
            Interface.save_position_to_button('x', Microscope_Base)

        if rb_button == 1 and y_button == 1:
            Interface.save_position_to_button('y', Microscope_Base)

        if rb_button == 1 and b_button == 1:
            Interface.save_position_to_button('b', Microscope_Base)

        if rb_button == 0 and a_button == 1:                               # Load functions
            Interface.load_position_from_button('a', Microscope_Base)

        if rb_button == 0 and x_button == 1:
            Interface.load_position_from_button('x', Microscope_Base)

        if rb_button == 0 and y_button == 1:
            Interface.load_position_from_button('y', Microscope_Base)

        if rb_button == 0 and b_button == 1:
            Interface.load_position_from_button('b', Microscope_Base)





        # ---------------------- MOVING THE MICROSCOPE BASE -----------------------------
        
        # Movement using keyboard / arrow keys
        if Interface.keys[pygame.K_LEFT]:
            x_change = -unit_change
        if Interface.keys[pygame.K_RIGHT]:
            x_change = unit_change
        if Interface.keys[pygame.K_DOWN]:
            y_change = unit_change
        if Interface.keys[pygame.K_UP]:
            y_change = -unit_change
            
        if Interface.keys[pygame.K_a]:
            x_change = -unit_change*100
        if Interface.keys[pygame.K_d]:
            x_change = unit_change*100
        if Interface.keys[pygame.K_w]:
            y_change = -unit_change*100
        if Interface.keys[pygame.K_s]:
            y_change = unit_change*100

        # Check if the user is no longer pressing a key
        if Interface.check_keyboard_key_up():
            x_change = 0
            y_change = 0

        # If using joystick, modify x_move and y_move accordingly
        if Interface.using_joystick:
            x_move_fine = Interface.get_joystick_xfine()         # Get fine changes
            y_move_fine = Interface.get_joystick_yfine()

            if abs(x_move_fine) >= 0.07:                         # Parse x fine
                x_change += int(x_move_fine * 10)
            else:
                x_change = 0
            if abs(y_move_fine) >= 0.07:                         # Parse y fine
                y_change += int(y_move_fine * 10)
            else:
                y_change = 0

            x_move = Interface.get_joystick_x()
            y_move = Interface.get_joystick_y()

            if abs(x_move) >= 0.07:                              # Parse x
                x_change = int(x_move * 100000)
            else:
                x_change += 0
            if abs(y_move) >= 0.07:                              # Parse y
                y_change = int(y_move * 100000)
            else:
                y_change += 0
                
        # Actually move the microscope base
        Microscope_Base.x_move_vel(x_change)
        Microscope_Base.y_move_vel(y_change)




        # ----------------------- UPDATE DISPLAY ACCORDINGLY --------------------------------
        Interface.refresh_pygame_display(Microscope_Base)

main()