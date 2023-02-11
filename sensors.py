import Adafruit_DHT
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class ReadSensors:

    def __init__(self):
        return self

    def getTempHumidity():
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = 4

        while True:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

            if humidity is not None and temperature is not None:
                return temperature, humidity
    
    def getSoilMoisture():
        
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.CE0)
        
        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)
        
        # create an analog input channel on pin 0
        chan = AnalogIn(mcp, MCP.P0)
        
        if True:
            rawADC, volt = chan.value, chan.voltage
            return rawADC, volt