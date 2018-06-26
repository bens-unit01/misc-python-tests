'''
Created on 17 juin 2018

@author: admin
'''
import os, sys
#from subprocess import call
import subprocess

class TestShell(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
       
 
    def test1(self):
        print("test_shell 1 ...")
        #subprocess.call("h.sh", shell=True)
        #os.system("cd C:\Users") 
        os.system("pwd") 
        os.system("ls -al") 
        print(sys.platform)


 