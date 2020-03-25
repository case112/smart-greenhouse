
import os
import time
import datetime
import glob
import MySQLdb
import json
import sys
import httplib
import socket
from time import strftime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-03168b33a0ff/w1_slave'

def tempRead():
    t = open(temp_sensor, 'r')
    lines = t.readlines()
    t.close()
 
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
    return round(temp_c,1)

temp = tempRead()

if temp > 0 or temp < 50:

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
            print temp
            datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
            print datetimeDB
            sql = "INSERT INTO waterTempData (datetime,sensor,temp) VALUES (%s,%s,%s)"

            try:
                print "Writing to DB"
                cur.execute(sql, (datetimeDB,sensor,temp))
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
        sensor = "1"
        datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        with open('logWater.txt', 'a') as fl:
            fl.write(datetimeDB)
            fl.write(',')
            fl.write(sensor)
            fl.write(',')
            fl.write(temp)
            fl.write('\n')
            print('Writes to log')
        
else:
    print "trying again next time"
    print temp
