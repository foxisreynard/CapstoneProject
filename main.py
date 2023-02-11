import sensors
import sys
from datetime import datetime
from pymongo import MongoClient


temp, rh = sensors.ReadSensors.getTempHumidity()
rh = round(rh,2) # bring RH to 2 decimal places.

rawADC, volt = sensors.ReadSensors.getSoilMoisture()

#get mongodb collection sorted
client = MongoClient("mongodb+srv://fox:capstone@capstoneproject.ybwmnir.mongodb.net/test")
db = client["CapstoneProject"]
collection = db["test"]

#1.3V is completely dry. 3.3V is submerged in water. 1.3V = 0%, 3.3V = 100%.
# Therefore we can use a linear equation to convert voltage to a percentage
# and then format the result to be pretty

soilMoisture = round(((volt - 3.3)/(1.3 - 3.3)*100),2)

#convert C to F
# and make it pretty
temp_f = round(((temp * 1.8) + 32),2)

# get time
timestamp = datetime.now()
if soilMoisture and temp and temp_f and rh is not None:
    data = {
        "_id": timestamp, #using timestamp as ID field. It will be unique every time. 
        "temp_c": temp,
        "temp_f": temp_f,
        "relative_humidity": rh,
        "soil_moisture": soilMoisture
    }
else: # add error logging
   
    old_stdout = sys.stdout

    log_file = open("py_data.log","w")

    sys.stdout = log_file

    print(timestamp + ":::::: VALUE DETECTION ERROR")

    sys.stdout = old_stdout

    log_file.close()


collection.insert_one(data)

####FOR TESTING###
#print(f"Temp is: {temp}\nHumidity is: {rh}%\nRawADC is:{rawADC}\nVoltage is:{volt}")
#print(f"soil moisture is {soilMoisture}")
