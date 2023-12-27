import influx_client
from influxdb_client import Point
import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)

client = influx_client.create_influx_client_from_env_settings()
write_api = client.write_api()

def write_to_db(value):
    p = Point("my_measurement").tag("location", "Hamburg").field("temperature", float(value))
    write_api.write(bucket="37C3", org="37C3", record=p)



while True:
    readout = str(ser.readline())
    readout = readout.split(":")[1]
    temp = readout.split(r"\t")[0]
    print(temp)
    write_to_db(temp)
    
