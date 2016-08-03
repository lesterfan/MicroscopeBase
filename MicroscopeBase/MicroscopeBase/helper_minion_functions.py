from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import time

def check_command_succeeded(reply):
    """
    Return true if command succeeded, print reason and return false if command
    rejected

    param reply: AsciiReply

    return: boolean
    """
    if reply.reply_flag != "OK": # If command not accepted (received "RJ")
        print ("Danger! Command rejected because: {}".format(reply.data))
        return False
    else: # Command was accepted
        return True

def parse_movement_unit_choice(input):
    '''
    Takes in a number from 1-6 and returns the change in units for each press
    of the arrow key, given that 1 microstep = 0.15625um

    param input: string

    return : int
    '''

    return{
        1:10,                          # 1.5625um
        2:1000,                        # 156.25um
        3:100000,                      # 15625um = 1.5625cm
        4:200000,                      # 31250um = 3.1250cm
        5:1,
        6:1
    }[input]