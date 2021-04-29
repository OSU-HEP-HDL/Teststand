import socket
import sys
from time import time, sleep

host = '10.206.68.18'

def connectiServer(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(1024)
        if data == "":
        sys.exit("no data received.")
    

def readiServer(hostname):
    temp = connectiServer(hostname, 1000, "*SRTF\r")
    temp = temp[1:-1]
    rh = connectiServer(hostname, 1000, "*SRH\r")
    rh = rh[1:-1]
    sleep(2)
    return temp, rh

if __name__ == '__main__':
        ts = ini(time())
        temp, rh = readiServer(host)