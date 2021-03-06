import socket
import sys
import time
import datetime
import re
from influxdb import InfluxDBClient

host = '10.206.70.13'
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
    while temp.decode('utf-8') is '':
        print("Couldn't get temperature. Re-trying.")
        temp = connectiServer(hostname, 1000, "*SRTF\r")
    temp = float(re.findall(r'[-+]?\d*\.\d+', temp.decode('utf-8'))[0])

    rh = connectiServer(hostname, 1000, "*SRH2\r")
    while rh.decode('utf-8') is '':
        print("Couldn't get humidity. Re-trying.")
        rh = connectiServer(hostname, 1000, "*SRH2\r")
    rh = float(re.findall(r'[-+]?\d*\.\d+', rh.decode('utf-8'))[0])

    return temp, rh

def uploaddata(temperature, humidity):
    """influxdb info format"""
    data_list = [{
        'measurement': 'teststand',
        'tags': {'cpu': 'aspen'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'iServer_temperature': temperature,
            'iServer_rh': humidity
            }
        }]

    return data_list


if __name__ == '__main__':
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('dcsDB')
    while True:
        temp, rh = readiServer(host)
        print('temperature: {} F, humidity = {} % RH '.format(temp, rh))
        client.write_points(uploaddata(temp, rh))
        time.sleep(3)

