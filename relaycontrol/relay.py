'''
Created on Jul 16, 2018

@author: osboxes
'''
import serial, sys 
from optparse import OptionParser

class Relay(object):
    
    def __init__(self):
       '''
       Constructor
       '''
    def printToScreen( self, msgstr):
        print "{0}\n".format(msgstr),
        no_op = 0
    # end printToScreen(msgstr):

    def initSerial(self):    
        NewSerialPort = serial.Serial()
        NewSerialPort.port = "/dev/ttyUSB0" 
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


    def test2(self):    
        print "test 2 ... start"

        print "test 2 ... end"

    def test1(self):
        print "test 1  ... start"
        NewSerialPort = self.initSerial()

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
 
        
      #  NewSerialPort.open()
        rList1 = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x30, 0x46, 0x46, 0x30, 0x30, 0x46, 0x45, 0x0D, 0x0A]
        rList2 = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x46, 0x44, 0x0D, 0x0A]
        rList3 = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x31, 0x46, 0x46, 0x30, 0x30, 0x46, 0x44, 0x0D, 0x0A]

        parser = OptionParser()
        parser.add_option("-d", "--device", action="store", type="string", dest="device", help="The device serial, example A6VV5PHY")
        parser.add_option("-l", "--list", action="store_true", dest="list", default=False, help="List all devices")
        parser.add_option("-r", "--relay", action="store", type="string", dest="relay", help="Relay to command by number: 1...8 or all")
        parser.add_option("-c", "--command", action="store", type="string", dest="command", help="State: on, off, state")
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose, print all info on screen")

        print(rList1)
        NewSerialPort.write(rList2)
        NewSerialPort.close() 
        print "test 1  ... end"
        
         
         

