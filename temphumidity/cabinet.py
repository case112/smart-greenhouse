import sys
import Adafruit_DHT
import time
import os
import MySQLdb
import json
import httplib
import socket

#Reads DHT22 in cabinet @GPIO port 27
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "27")

print humidity
print temperature
time.sleep(5)

#Repeats for better measurements
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "27")

temp = float(temperature)
hum = float(humidity)

temp = round(temp,1)
hum = round(hum,1)

print hum
print temp

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
        sensor = "1"
        datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        print hum
        print temp
        print datetimeDB
        sql = "INSERT INTO hardwareTempHum (datetime,sensor,temp,hum) VALUES (%s,%s,%s,%s)"
        try:
            print "Writing to DB"
            cur.execute(sql, (datetimeDB,sensor,temp,hum))
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
    temp = str(temp)
    hum = str(hum)
    sensor = "1"
    datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    with open('logCabinet.txt', 'a') as fl:
        fl.write(datetimeDB)
        fl.write(',')
        fl.write(sensor)
        fl.write(',')
        fl.write(temp)
        fl.write(',')
        fl.write(hum)
        fl.write('\n')
        print('Writes to log')
        