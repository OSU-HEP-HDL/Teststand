import pyvisa as visa
from influxdb import InfluxDBClient
import datetime
import time

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

rm = visa.ResourceManager()
DAQ = rm.open_resource('TCPIP::k-daq970a-01258.dhcp.okstate.edu::inst0::INSTR')
PS = rm.open_resource('TCPIP::K-E36233A-09066.dhcp.okstate.edu::inst0::INSTR')
print(DAQ.query('*IDN?'))

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
