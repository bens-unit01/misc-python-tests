'''
Created on Jul 16, 2018

@author: osboxes
'''
import serial 

class Relay(object):
    
    def __init__(self):
       '''
       Constructor
       '''
    def printToScreen( self, msgstr):
        print "{0}\n".format(msgstr),
        no_op = 0
    # end printToScreen(msgstr):

  
        
    def test1(self):
        print "test 1  ... start"
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

        if (NewSerialPort.isOpen() == False):
            try:
                NewSerialPort.open()
                print( "Serial port opened")
            except Exception as e:
                print( "error open serial port: " + str(e))
        else:
            print( "Serial port already open???")

        NewSerialPort.flushInput() #flush input buffer, discarding all its contents
        NewSerialPort.flushOutput()#flush output buffer, aborting current output
 
        
      #  NewSerialPort.open()
        rList1 = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x30, 0x46, 0x46, 0x30, 0x30, 0x46, 0x45, 0x0D, 0x0A]
        rList2 = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x46, 0x44, 0x0D, 0x0A]
        rList3 = [0x3A, 0x46, 0x45, 0x30, 0x35, 0x30, 0x30, 0x30, 0x31, 0x46, 0x46, 0x30, 0x30, 0x46, 0x44, 0x0D, 0x0A]

        print(rList2)
        NewSerialPort.write(rList2)
        NewSerialPort.close() 
        print "test 1  ... end"
        
         
         

