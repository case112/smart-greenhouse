##Chirp library from https://github.com/ageir/chirp-rpi must be included 

import chirp
import time
import sys
import os
import MySQLdb
import json
import httplib
import socket

sensor20= "20"
sensor21= "21"

# These values needs to be calibrated for the percentage to work!
#For sensor 20
min_moist20 = 245
max_moist20 = 655

#For sensor 21
min_moist21 = 260
max_moist21 = 579

# Initialize the sensor
chirp20 = chirp.Chirp(address=0x20,
                    read_moist=True,
                    read_temp=True,
                    read_light=False,
                    min_moist=min_moist20,
                    max_moist=max_moist20,
                    temp_scale='celsius',
                    temp_offset=0)

# Initialize the sensor
chirp21 = chirp.Chirp(address=0x21,
                    read_moist=True,
                    read_temp=True,
                    read_light=True,
                    min_moist=min_moist21,
                    max_moist=max_moist21,
                    temp_scale='celsius',
                    temp_offset=0)

try:
    # Trigger the sensors and take measurements.
    chirp20.trigger()
    chirp21.trigger()

    moist20=chirp20.moist
    perc20=chirp20.moist_percent
    temp20=chirp20.temp

    moist21=chirp21.moist
    perc21=chirp21.moist_percent
    temp21=chirp21.temp

    print ('Testing')
    print moist20
    print perc20
    print temp20
    print ('-')
    print moist21
    print perc21
    print temp21
    print ('-')


    time.sleep(5)
    # Trigger the sensors and take measurements.
    chirp20.trigger()
    chirp21.trigger()

    moist20=chirp20.moist
    perc20=chirp20.moist_percent
    temp20=chirp20.temp

    moist21=chirp21.moist
    perc21=chirp21.moist_percent
    temp21=chirp21.temp

    
    temp20=float(temp20)
    temp20= temp20 - 2
    temp21=float(temp21)
    temp21= temp21 - 2

    print ('Saving these')
    print moist20
    print perc20
    print temp20
    print ('-')
    print moist21
    print perc21
    print temp21
    print ('-')

finally:
    print('-')

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
        print datetimeDB
        sql = "INSERT INTO soil (datetime,sensor,moisture,moistureperc,temp) VALUES (%s,%s,%s,%s,%s)"
        try:
            print "Writing to DB"
            cur.execute(sql, (datetimeDB,sensor20,moist20,perc20,temp20))
            cur.execute(sql, (datetimeDB,sensor21,moist21,perc21,temp21))
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

    moist20=str(moist20)
    perc20=str(perc20)
    temp20=str(temp20)
    moist21=str(moist21)
    perc21=str(perc21)
    temp21=str(temp21)
    
    datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    with open('logSoil.txt', 'a') as fl:
        #Sensor 1
        fl.write(datetimeDB)
        fl.write(',')
        fl.write(sensor20)
        fl.write(',')
        fl.write(moist20)
        fl.write(',')
        fl.write(perc20)
        fl.write(',')
        fl.write(temp20)
        fl.write('\n')
        #Sensor 2
        fl.write(datetimeDB)
        fl.write(',')
        fl.write(sensor21)
        fl.write(',')
        fl.write(moist21)
        fl.write(',')
        fl.write(perc21)
        fl.write(',')
        fl.write(temp21)
        fl.write('\n')
        print('Writes to log')

