import serial
import zaber.serial                     # The library for writing to Zaber software
from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand

# Please see http://www.zaber.com/wiki/Manuals/ASCII_Protocol_Manual under "Making it Move"
# to familiarize yourself with ASCII protocol for communicating with the device
# See http://www.zaber.com/support/docs/api/core-python/0.8.1/getting-started.html to further
# familiarize yourself with how the Zaber software works.

def main():
    

    # ------------------------------------- Serial ---------------------------------------
    # The Serial classes, AsciiSerial and BinarySerial are the core of the library
    # They are used to communicate with the serial port, and other classes in the library
    # take them as constructor arguments.
    # Create a new instance like this : ser = AsciiSerial("COM1")
    ser = AsciiSerial("COM1")

    
    # ------------------------------------- Device ---------------------------------------
    # The device classes are used to represent individual Zaber devices. A Device allows
    # you to interact with Zaber devices directly in your code. 
    # Create a new device like this : device = AsciiDevice(ser, 23)
    device = AsciiDevice(ser, 1)

    # There are functions such as device.home() <-> device.send("home")
    # This sends the device back "home", eg moves it



    # ------------------------------------- Commands ---------------------------------------
    # We use the AsciiCommand(device number, command text, data value) to pass commands to 
    # the devices.
    # Eg : moverel_cmd = AsciiCommand(1, "move rel", 1000)
    # or : moverel_cmd2 = AsciiCommand("1 move rel 1000")
    
    moverel_cmd = AsciiCommand(1, "move rel", 1000)

    # After we have the Command, we can pass it to the Serial object to tbe transmitted.
    # Eg : ser.write(moverel_cmd)
    
    # Alternatively, we can pass it to a Device
    # Eg : device.send(moverel_cmd)

    device.send(moverel_cmd)


    
    
    # ------------------------------------- Reply ---------------------------------------
    # The Reply class represent replies received from Zaber devices. Many functions in 
    # this library return AsciiReply or BinaryReply objects.
    # Please see http://www.zaber.com/support/docs/api/core-python/0.8.1/examples.html 
    # for a more complete documentation of replies / and the rest of the software



    # ------------------------------------- Extra --------------------------------------

    # Some devices may have multiple axes. 
    # Just as an AsciiDevice models a single Zaber device using the ASCII protocol, an
    # AsciiAxis models a single AXIS of a Zaber device.

    # This specific device ALSO supports micro-manager at https://micro-manager.org/


    print ("hello, microscope!")

main()