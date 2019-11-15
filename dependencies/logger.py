#!/usr/bin/python
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
    


def dump(msg, msg_type):
    try:
        msg = msg.decode('utf8', errors='ignore')
    except:
        pass
    

    if msg_type == "critical": 
        print(bcolors.FAIL + msg + bcolors.ENDC)
    
    
    if msg_type == "error":    
        print(bcolors.ERROR + msg + bcolors.ENDC)
    

    if msg_type == "warning":    
        print(bcolors.WARNING + msg + bcolors.ENDC)
    


    if msg_type == "info":     
        print(bcolors.OKBLUE + msg + bcolors.ENDC)
    

    if msg_type == "good":     
        print(bcolors.OKGREEN + msg + bcolors.ENDC)
    

    if msg_type == "debug":     
        print(bcolors.HEADER + msg + bcolors.ENDC)
    

