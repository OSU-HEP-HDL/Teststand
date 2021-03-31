import pyvisa as visa
from influxdb import InfluxDBClient
import datetime
import time
import sys

def upload(temp, voltage, current):
    """influxdb info format"""
    data_list = [{
        'measurement': 'teststand',
        'tags': {'cpu': 'aspen'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'temperature': temp,
            'voltage': voltage,
            'current': current
            }
        }]

    return data_list

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('dcsDB')

DAQ_visa = 'TCPIP::k-daq970a-01258.dhcp.okstate.edu::inst0::INSTR'
PS_visa = 'TCPIP::K-E36233A-09066.dhcp.okstate.edu::inst0::INSTR'

rm = visa.ResourceManager()
try:
    DAQ = rm.open_resource(DAQ_visa)
except visa.Error as ex:
    print("couldn't connect to DAQ. Please make sure your devide is on and the visa address is correct")
try:
    PS = rm.open_resource(PS_visa)
except visa.Error as ex:
    print("couldn't connect to Power Supply. Please make sure your devide is on and the visa address is correct")

while True:
    DAQ.write("MEAS:TEMP? (@101)")
    temp = float(DAQ.read())
    PS.write("MEAS:VOLT?")
    Voltage = float(PS.read())
    PS.write("MEAS:CURR?")
    Current = float(PS.read())
    print(temp, Voltage, Current)
    client.write_points(upload(temp, Voltage, Current))
    time.sleep(3)
