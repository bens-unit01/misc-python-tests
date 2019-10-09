#!C:/Python37/python
# coding=UTF-8

# ----------------------------------------------------------------------------
#
#   DRCONTROL.PY
#
#   Copyright (C) 2012 Sebastian Sjoholm, sebastian.sjoholm@gmail.com
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Original Version history can be found at
#   http://code.google.com/p/drcontrol/wiki/VersionHistory
#
#
# ----------------------------------------------------------------------------

from optparse import OptionParser

from pylibftdi import Driver
from pylibftdi import BitBangDevice

from ctypes.util import find_library

import sys
import time
import serial

# ----------------------------------------------------------------------------
# VARIABLE CLASSS
# ----------------------------------------------------------------------------

class app_data:
    def __init__(
        self,
        name = "DRControl",
        version = "0.13",
        date = "$Date: 2013-01-03 18:13:01 +0100 (Thu, 03 Jan 2013) $",
        rev = "$Rev: 53 $",
        author = "Sebastian Sjoholm"
        ):

        self.name = name
        self.version = version
        self.build = date
        self.rev = rev
        self.author = author

class cmdarg_data:
    def __init__(
        self,
        device = "",
        relay = "",
        command = "",
        verbose = False
        ):

        self.device = device
        self.relay = relay
        self.command = command
        self.verbose = verbose

class relay_data(dict):

    address = {
            "1":"1",
            "2":"2",
            "3":"4",
            "4":"8",
            "5":"10",
            "6":"20",
            "7":"40",
            "8":"80",
            "all":"FF"
            }

    def __getitem__(self, key): return self[key]
    def keys(self): return self.keys()

# ----------------------------------------------------------------------------
# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
# http://wiki.python.org/moin/BitManipulation
# ----------------------------------------------------------------------------

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

def get_relay_state( data, relay ):
    if relay == "1":
        return testBit(data, 1)
    if relay == "2":
        return testBit(data, 3)
    if relay == "3":
        return testBit(data, 5)
    if relay == "4":
        return testBit(data, 7)
    if relay == "5":
        return testBit(data, 2)
    if relay == "6":
        return testBit(data, 4)
    if relay == "7":
        return testBit(data, 6)
    if relay == "8":
        return testBit(data, 8)

# ----------------------------------------------------------------------------
# LIST_DEVICES()
#
# Routine modified from the original pylibftdi example by Ben Bass
# ----------------------------------------------------------------------------

def list_devices():
    print("Vendor\t\tProduct\t\t\tSerial")
    dev_list = []
    for device in Driver().list_devices():
        device = map(lambda x: x.decode('latin1'), device)
        vendor, product, serial = device
        #print "%s\t\t%s\t\t%s" % (vendor, product, serial)
        print(vendor, "\t" , product, "\t", serial)



def init_serial(port):    
    NewSerialPort = serial.Serial()
    NewSerialPort.port = port 
    NewSerialPort.baudrate = 9600 
    NewSerialPort.bytesize = serial.EIGHTBITS     #number of bits per bytes
    NewSerialPort.parity = serial.PARITY_NONE     #set parity check: no parity
    NewSerialPort.stopbits = serial.STOPBITS_ONE  #number of stop bits
    NewSerialPort.timeout = 4                     #non-block read
    NewSerialPort.xonxoff = False                 #disable software flow control
    NewSerialPort.rtscts = False                  #disable hardware (RTS/CTS) flow control
    NewSerialPort.dsrdtr = False                  #disable hardware (DSR/DTR) flow control
    NewSerialPort.writeTimeout = 2                #timeout for write
    return NewSerialPort

# ----------------------------------------------------------------------------
# SET_RELAY()
#
# Set specified relay to chosen state
# ----------------------------------------------------------------------------

def set_relay_16ch():
## Making the command vector
    command_vector = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x30, 0x46, 0x46, 0x30, 0x30, 0x46, 0x45, 0x0D, 0x0A]
    on     = [0x45, 0x44, 0x43, 0x42, 0x41, 0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30, 0x46]
    off    = [0x44, 0x43, 0x42, 0x41, 0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30, 0x46, 0x45]
    all_on = [0x3A, 0x46, 0x45, 0x30, 0x46, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x31, 0x30, 0x30, 0x32, 0x46, 0x46, 0x46, 0x46, 0x45, 0x33, 0x0D, 0x0A]
    all_off = [0x3A, 0x46, 0x45, 0x30, 0x46, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x31, 0x30, 0x30, 0x32, 0x30, 0x30, 0x30, 0x30, 0x45, 0x31, 0x0D, 0x0A]

    print command_vector 
    print " ".join(hex(n) for n in command_vector)
    print "-- --"
    print cmdarg.relay
    if(cmdarg.relay == 'all'):
        if(cmdarg.command == 'off'): 
           command_vector = all_off;  
        else: 
            command_vector = all_on
    else:
        command_vector[8] = 0x30 + int(cmdarg.relay) -1; 
        command_vector[9] = 0x46 if (cmdarg.command == 'on') else 0x30; 
        command_vector[10] =  command_vector[9]

        if int(cmdarg.relay) >= 11:
            command_vector[8] += 7; 

        if cmdarg.command == "on":
            command_vector[14] = on[int(cmdarg.relay) -1]
        else:
            command_vector[14] = off[int(cmdarg.relay) -1]

    print " ".join(hex(n) for n in command_vector)


## Sending command to the relay 
    NewSerialPort = init_serial(cmdarg.device)
    if (NewSerialPort.isOpen() == False):
        try:
            NewSerialPort.open()
            print( "Serial port opened")
        except Exception as e:
            print( "error open serial port: " + str(e))
            sys.exit(0)

    else:
        print( "Serial port already open???")
        NewSerialPort.flushInput() #flush input buffer, discarding all its contents
        NewSerialPort.flushOutput()#flush output buffer, aborting current output


    NewSerialPort.write(command_vector)
    NewSerialPort.close() 
    print "test 1  ... end"

 

def set_relay_8ch():

    if cmdarg.verbose:
        print("Device:\t\t", cmdarg.device)
        print("Send command:\tRelay " , cmdarg.relay , " (0x" , relay.address[cmdarg.relay] , ") to " , cmdarg.command.upper())

    try:
        with BitBangDevice(cmdarg.device) as bb:

            # Action towards specific relay
            if cmdarg.relay.isdigit():

                if int(cmdarg.relay) >= 1 and int(cmdarg.relay) <= 8:

                    # Turn relay ON
                    if cmdarg.command == "on":
                        if cmdarg.verbose:
                            print("Relay " , str(cmdarg.relay) , " to ON")
                        bb.port |= int(relay.address[cmdarg.relay], 16)

                    # Turn relay OFF
                    elif cmdarg.command == "off":
                        if cmdarg.verbose:
                            print("Relay "  , str(cmdarg.relay) , " to OFF")
                        bb.port &= ~int(relay.address[cmdarg.relay], 16)

                    # Print relay status
                    elif cmdarg.command == "state":
                        state = get_relay_state( bb.port, cmdarg.relay )
                        if state == 0:
                            if cmdarg.verbose:
                                print("Relay " , cmdarg.relay , " state:\tOFF (" , str(state) , ")")
                            else:
                                print("OFF")
                        else:
                            if cmdarg.verbose:
                                print("Relay " , cmdarg.relay , " state:\tON (" , str(state) , ")")
                            else:
                                print("ON")

            # Action towards all relays
            elif cmdarg.relay == "all":

                if cmdarg.command == "on":
                    if cmdarg.verbose:
                        print("Relay " , str(cmdarg.relay) , " to ON")
                    bb.port |= int(relay.address[cmdarg.relay], 16)

                elif cmdarg.command == "off":
                    if cmdarg.verbose:
                        print("Relay "  , str(cmdarg.relay) , " to OFF")
                    bb.port &= ~int(relay.address[cmdarg.relay], 16)

                elif cmdarg.command == "state":
                    for i in range(1,8):
                        state = get_relay_state( bb.port, str(i) )
                        if state == 0:
                            if cmdarg.verbose:
                                print("Relay " , str(i) , " state:\tOFF (" , str(state) , ")")
                            else:
                                print("OFF")
                        else:
                            if cmdarg.verbose:
                                print("Relay " , str(i) , " state:\tON (" , str(state) , ")")
                            else:
                                print("ON")

                else:
                    print("Error: Unknown command")

            else:
                print("Error: Unknown relay number")
                sys.exit(1)

    except Exception as err:
        print("Error: " , str(err))
        sys.exit(1)

#def check():

    # Check python version
#    if sys.hexversion < 0x03040000:
#        print("Error: Your Python need to be 3.4 or newer")
#        sys.exit(1)

    #Check availability on library, this check is also done in pylibftdi
    #ftdi_lib = find_library('libftdi1')
    #if ftdi_lib is None:
    #   print("Error: libftdi library not found")
    #   sys.exit(1)

if __name__ == '__main__':

    # Init objects
    cmdarg = cmdarg_data()
    relay = relay_data()
    app = app_data()

    # Do system check
#    check()

    parser = OptionParser()
    parser.add_option("-d", "--device", action="store", type="string", dest="device", help="The device serial, example A6VV5PHY")
    parser.add_option("-l", "--list", action="store_true", dest="list", default=False, help="List all devices")
    parser.add_option("-r", "--relay", action="store", type="string", dest="relay", help="Relay to command by number: 1...8 or all")
    parser.add_option("-c", "--command", action="store", type="string", dest="command", help="State: on, off, state")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose, print all info on screen")
    parser.add_option("-t", "--type", action="store", type="string", dest="type", help="Relay type, 8 or 16 channel relay")

    (options, args) = parser.parse_args()
   
    print  options
    print  args 

    if options.verbose:
        cmdarg.verbose = options.verbose
        print(app.name , " " , app.version)
    else:
        cmdarg.verbose = False

    if options.list:
        list_devices()
        sys.exit(0)

    if options.relay or options.command:
        if not options.device:
            print("Error: Device missing")


    if options.type:
        if options.device:
            if not options.relay:
                print("Error: Need to state which relay")
                sys.exit(1)
            if not options.command:
                print("Error: Need to specify which relay state")
                sys.exit(1)

        cmdarg.device = options.device
        cmdarg.relay = options.relay.lower()
        cmdarg.command = options.command.lower()

        if options.type == "16":
            print " 16 channel relay" 
            set_relay_16ch()
        else: 
            print " 8 channel relay" 
            set_relay_8ch()

        sys.exit(0)












