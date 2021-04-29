import socket
import sys
from time import time, sleep
import re

host = '10.206.68.18'
# iServer ip address

def connectiServer(hostname, port, content):
    ''' connect to iServer and access temperature/RH'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content.encode('utf-8'))
    s.shutdown(socket.SHUT_WR)
    data = s.recv(1024)
    s.close()
    return data
    

def readiServer(hostname):
    ''' read temperature/RH value from iServer  '''
    temp = connectiServer(hostname, 1000, "*SRTF\r")
    try:
        temp = float(re.findall(r'[-+]?\d*\.\d+', temp.decode('utf-8'))[0])
    except IndexError:
        print('No temperature value found.')

    rh = connectiServer(hostname, 1000, "*SRH2\r")
    try:
        rh = float(re.findall(r'[-+]?\d*\.\d+', rh.decode('utf-8'))[0])
    except IndexError:
        print('No humidity value found.')
    sleep(2)
    return temp, rh

if __name__ == '__main__':
        temp, rh = readiServer(host)
