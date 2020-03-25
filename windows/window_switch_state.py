import RPi.GPIO as gpio
import sys
import time
import os
import MySQLdb
import json
import httplib
import socket

state=99

gpio.setmode(gpio.BCM)
gpio.setup(16, gpio.IN, gpio.PUD_UP)
gpio.setup(24, gpio.IN, gpio.PUD_UP)

if gpio.input(16) == 1 and gpio.input(24) == 1:
    print "window open"
    state = 1
    gpio.cleanup()
else:
    print "window closed"
    state = 0
    gpio.cleanup()

#Repeat for better measurements
state=99
gpio.setmode(gpio.BCM)
gpio.setup(16, gpio.IN, gpio.PUD_UP)
gpio.setup(24, gpio.IN, gpio.PUD_UP)

if gpio.input(16) == 1 and gpio.input(24) == 1:
    print "window open"
    state = 1
    gpio.cleanup()
else:
    print "window closed"
    state = 0
    gpio.cleanup()

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
        switch = "both"
        db = MySQLdb.connect(host, user, password, database)
        cur = db.cursor()
        datetimeDB = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        #print hum
        #print temp
        print datetimeDB
        sql = "INSERT INTO windows (datetime,switch,state) VALUES (%s,%s,%s)"
        try:
            print "Writing to DB"
            cur.execute(sql, (datetimeDB,switch,state))
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
    print "Try again later"
        