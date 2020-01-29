'''
Created on Jul 10, 2018

@author: Geothentic-DEV
'''
import time
import usb.core
import usb.util
import usb.backend
import os

def get_backend_libusb01():
    libusb01_location = os.getcwd()

    # load-library (ctypes.util.find_library) workaround: also search the current folder
    is_current_folder_in_search_path = True
    ''' if None == usb.backend.libusb0.get_backend():
        is_current_folder_in_search_path = libusb01_location in os.environ['PATH']
        if not is_current_folder_in_search_path:
            os.environ['PATH'] += os.pathsep + libusb01_location

    backend = usb.backend.libusb0.get_backend()

    if not is_current_folder_in_search_path:
        os.environ['PATH'] = os.environ['PATH'].replace(os.pathsep + libusb01_location, "")
    '''

    return usb.backend.libusb1 

if __name__ == '__main__':
#    dev = usb.core.find(idVendor=0x1a86, idProduct=0x7523)
#    dev = usb.core.find(find_all=True)
    print(get_backend_libusb01())
    pass