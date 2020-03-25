import sys
import Adafruit_DHT
import time
import os
import MySQLdb
import json
import httplib
import socket

#Reads DHT22 inside GH @ GPIO port 17
humidity1, temperature1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "17")
#Reads DHT22 inside GH @ GPIO port 22
humidity2, temperature2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "22")

sensor1 = "Right"
sensor2 = "Left"

print humidity1
print temperature1

print humidity2
print temperature2

time.sleep(5)

#Repeats for better measurements
humidity1, temperature1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "17")
humidity2, temperature2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "22")

temp1 = float(temperature1)
hum1 = float(humidity1)
temp2 = float(temperature2)
hum2 = float(humidity2)

temp1 = round(temp1,1)
hum1 = round(hum1,1)
temp2 = round(temp2,1)
hum2 = round(hum2,1)

print hum1
print temp1
print hum2
print temp2

#Check if there is internet connection
con_url = "www.google.com"
con_resouce = "/intl/en/policies/privacy/"
test_con = httplib.HTTPConnection(con_url)
connection = 0

try:
    test_con.request("GET", con_resouce)
    response = test_con.getresponse()
except httplib.ResponseNotReady as e:
    print "Improper connection state"
except socket.gaierror as e:
    print "Not connected"
else:
    connection = 1
    print "Connected"

test_con.close()

#If there is internet connection then uploads to DB 
if connection == 1:
    #Getting info from config file
    def getConfigurations():
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        configurationFile = path + '/../config.json'
        configurations = json.loads(open(configurationFile).read())

        return configurations

    #DB variables
    configurations = getConfigurations()
    host = configurations["mysql"][0]["host"]
    user = configurations["mysql"][0]["user"]
    password = configurations["mysql"][0]["password"]
    database = configurations["mysql"][0]["database"]

    #Tries to write to DB
    while True:
        db = MySQLdb.connect(host, user, password, database)
        cur = db.cursor()
        datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        #print hum
        #print temp
        print datetimeDB
        sql = "INSERT INTO tempHum (datetime,sensor,temp,hum) VALUES (%s,%s,%s,%s)"
        try:
            print "Writing to DB"
            cur.execute(sql, (datetimeDB,sensor1,temp1,hum1))
            cur.execute(sql, (datetimeDB,sensor2,temp2,hum2))
            db.commit()
            print "Done"
     
        except:
            # Rollback if error
            db.rollback()
            print "Error"
     
        cur.close()
        db.close()
        break

else:
    temp1 = str(temp1)
    hum1 = str(hum1)
    temp2 = str(temp2)
    hum2 = str(hum2)
    datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    with open('logTempHum.txt', 'a') as fl:
        #Sensor 1
        fl.write(datetimeDB)
        fl.write(',')
        fl.write(sensor1)
        fl.write(',')
        fl.write(temp1)
        fl.write(',')
        fl.write(hum1)
        fl.write('\n')
        #Sensor 2
        fl.write(datetimeDB)
        fl.write(',')
        fl.write(sensor2)
        fl.write(',')
        fl.write(temp2)
        fl.write(',')
        fl.write(hum2)
        fl.write('\n')
        print('Writes to log')
        
