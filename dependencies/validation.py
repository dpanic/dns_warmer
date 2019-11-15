#!/usr/bin/python3
import sys
import ipaddress

class validation:

    def __init__(self):
        pass



    #
    # Check if input is IP
    #
    def is_ip(self, ip):
        try:
            tmp = ipaddress.IPv4Address(ip)
            return True
        except:
            #print(str(sys.exc_info()))
            return False
        
        return False
    



if __name__ == '__main__':
    v = validation()
    print(v.is_ip('127.0.0.1'))
    print(v.is_ip('false'))
    print(v.is_ip('222.222.222.222'))
    print(v.is_ip('1.1.1.1'))




