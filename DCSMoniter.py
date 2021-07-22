import pyvisa as visa
from influxdb import InfluxDBClient
import datetime
import time
import sys
import serial

def upload(temp, airTemp, airHumid, voltage, current):
    """influxdb info format"""
    data_list = [{
        'measurement': 'teststand',
        'tags': {'cpu': 'aspen'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'ModuleTemperature': temp,
            'AirTemperature': airTemp,
            'AirHumidity': airHumid,
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
#try:
#    DAQ = rm.open_resource(DAQ_visa)
#except visa.Error as ex:
#    print("couldn't connect to DAQ. Please make sure your devide is on and the visa address is correct")
try:
    PS = rm.open_resource(PS_visa)
except visa.Error as ex:
    print("couldn't connect to Power Supply. Please make sure your devide is on and the visa address is correct")

while True:
    #DAQ.write("MEAS:TEMP? (@101)")
    #temp = float(DAQ.read())
    # get module temperature from Arduino readout
    ser = serial.Serial('/dev/ttyACM0', 9600)
    b = ser.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    try:
        temp, airTemp, airHumid = string.split()
    except ValueError:
        print("Ooooops! Arduino is doing something stupid! Try again...")
    PS.write("MEAS:VOLT? (@1)")
    Voltage = float(PS.read())
    PS.write("MEAS:CURR? (@1)")
    Current = float(PS.read())
    print(temp, airTemp, airHumid, Voltage, Current)

    # interlock
    # if module temperature above threshold, turn off module
    if float(temp) > 40 and Voltage != 0:
        PS.write("VOLT:LEV 0, (@1)")

    client.write_points(upload(float(temp), float(airTemp), float(airHumid), Voltage, Current))
    time.sleep(3)
