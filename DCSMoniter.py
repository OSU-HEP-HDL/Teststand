import pyvisa as visa
from influxdb import InfluxDBClient
import datetime
import time

def upload(temp):
    """influxdb info format"""
    data_list = [{
        'measurement': 'teststand',
        'tags': {'cpu': 'aspen'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'temperature': temp
            }
        }]

    return data_list

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('dcsDB')

rm = visa.ResourceManager()
DAQ = rm.open_resource('TCPIP::k-daq970a-01258.dhcp.okstate.edu::inst0::INSTR')
print(DAQ.query('*IDN?'))

while True:
    DAQ.write("MEAS:TEMP? (@101)")
    temp = float(DAQ.read())
    print(temp)
    client.write_points(upload(temp))
    time.sleep(3)
