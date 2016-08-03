from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply, AsciiAxis
import time

# Helper to check that commands succeeded.
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


# Open a serial port. You may need to edit this section for your particular
# hardware and OS setup.
#port = AsciiSerial("/dev/ttyUSB0")  # Linux
port = AsciiSerial("COM3")         # Windows

# Get a handle for device #1 on the serial chain. This assumes you have a
# device already in ASCII 115,220 baud mode at address 1 on your port.
device = AsciiDevice(port, 1) # Device number 1
test_x = AsciiAxis(device, 1)
test_y = AsciiAxis(device, 2)
test_z = AsciiAxis(device, 3)



# Make the device has finished its previous move before sending the
# next command. Note that this is unnecessary in this case as the
# AsciiDevice.home command is blocking, but this would be required if
# the AsciiDevice.send command is used to trigger movement.
device.poll_until_idle()

# Now move the device to a non-home position.
#reply = test_x.move_rel(200000) # move rel 2000 microsteps
#
#if not check_command_succeeded(reply):
#    print("Device move failed.")
#    exit(1)
#
## Wait for the move to finish.
#device.poll_until_idle()

# reply = test_y.move_rel(80000) # move rel 2000 microsteps
# 
# if not check_command_succeeded(reply):
#     print("Device move failed.")
#     exit(1)
# 
# # Wait for the move to finish.
# device.poll_until_idle()

# Read back what position the device thinks it's at.
reply = device.send("get pos")
print("Device position is now " + reply.data)

    
# Home the device and check the result.
reply = device.home()
if check_command_succeeded(reply):
    print("Device Homed.")
else:
    print("Device home failed.")
    exit(1)
# Wait for the move to finish.
device.poll_until_idle()


# Clean up.
port.close()