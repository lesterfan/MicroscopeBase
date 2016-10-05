
from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply, AsciiAxis

class MicroscopeBase:

    """ Encapsulated version of the zaber microscope class. Allows for two degrees of 
    freedom in movement as well as the ability to save/return to locations """

    # Defining self variables

    mAsciiSerial = None                  # The serial port
    mAsciiDevice = None                  # The reference to the microscope object

    x_axis = None                       # The reference to the x axis object
    y_axis = None                       # The reference to the y axis object

    mLastRet = 0                         # Will be 1 if there was an error in the last operation done



    ''' 
    Constructor that sets up connection to the microscope base. Instantiates all the 
    internal variables
    @ param serial_port : String describing the port that the base is connected to, eg "COM5"
    Returns None
    '''
    def __init__(self, serial_port_string):
        try:
            # Connect to serial
            self.mAsciiSerial = AsciiSerial(serial_port_string)

            # Connect to device
            self.mAsciiDevice = AsciiDevice(self.mAsciiSerial, 1)

            # Establish axes
            self.x_axis = AsciiAxis(self.mAsciiDevice, 1)
            self.y_axis = AsciiAxis(self.mAsciiDevice, 2)

            mLastRet = 0

        except Exception as e:
            print "Error! ", e
            mLastRet = 1

            return

    
    '''
    Returns a tuple representing the absolute location of the device right now
    Returns (int, int) representing (location_x, location_y)
    '''
    def get_absolute_position(self):
    
        reply = self.mAsciiDevice.send("get pos")
        position_array = reply.data.split()
        x_curr = int(position_array[0])
        y_curr = int(position_array[1])
        mLastRet = 0
    
        return (x_curr, y_curr)


    '''
    Internal helper function that returns true if command succeeded, print reason and return false if command
    rejected
    @param reply: AsciiReply
    Returns Boolean
    '''
    def check_command_succeeded(self, reply):
        if reply.reply_flag != "OK": # If command not accepted (received "RJ")
            print ("Danger! Command rejected because: {}".format(reply.data))
            return False
        else: # Command was accepted
            return True

    '''
    Moves the x axis of the microscope base num amount of microsteps
    @param num : number of microsteps to be moved
    Returns : None
    '''
    def x_move_rel(self, num):
        reply = self.x_axis.move_rel(num)
        if not self.check_command_succeeded(reply):
            self.mLastRet = 1
            print "Command failed in x_move_rel!"
            return
        self.mLastRet = 0    

    '''
    Moves the y axis of the microscope base num amount of microsteps
    @param num : number of microsteps to be moved
    Returns : None
    '''
    def y_move_rel(self, num):
        reply = self.y_axis.move_rel(num)
        if not self.check_command_succeeded(reply):
            self.mLastRet = 1
            print "Command failed in y_move_rel!"
            return
        self.mLastRet = 0


    ''' 
    Moves the x axis of the microscope base to the coordinate defined by x_coord
    @ param x_coord : int that describes the desired location of the x axis
    Returns None
    '''
    def x_move_abs(self, x_coord):
        reply = self.x_axis.move_abs(x_coord)
        if not self.check_command_succeeded(reply):
            self.mLastRet = 1
            print "Command failed in x_move_abs!"
            return
        self.mLastRet = 0


    ''' 
    Moves the y axis of the microscope base to the coordinate defined by y_coord
    @ param x_coord : int that describes the desired location of the y axis
    Returns None
    '''
    def y_move_abs(self,y_coord):
        reply = self.y_axis.move_abs(y_coord)
        if not self.check_command_succeeded(reply):
            self.mLastRet = 1
            print "Command failed in y_move_abs!"
            return
        self.mLastRet = 0
        

    ''' 
    Moves the x axis of the microscope according to the speed set by input_speed
    @ param input_speed : int that describes the desired speed that the x axis should move
    Returns None
    '''
    def x_move_vel(self,input_speed):
        reply = self.x_axis.move_vel(input_speed)
        if not self.check_command_succeeded(reply):
            self.mLastRet = 1
            print "Command failed in x_move_vel!"
            return
        self.mLastRet = 0        
        

    ''' 
    Moves the y axis of the microscope according to the speed set by input_speed
    @ param input_speed : int that describes the desired speed that the y axis should move
    Returns None
    '''
    def y_move_vel(self,input_speed):
        reply = self.y_axis.move_vel(input_speed)
        if not self.check_command_succeeded(reply):
            self.mLastRet = 1
            print "Command failed in y_move_vel!"
            return
        self.mLastRet = 0


    ''' 
    Homes the device. Ensures that the internal x and y coordinates are accurate
    '''
    def home_device(self):
        reply = self.mAsciiDevice.home()
        if not self.check_command_succeeded(reply):
            print "Device home failed!"
            self.mLastRet = 1
            return
        self.mLastRet = 0


