import RPi.GPIO as gpio
import time
import datetime
import sys
import os
import MySQLdb
import json
import httplib
import socket

data = []
temp1 = 0
temp2 = 0
hum1 = 0
hum2 = 0
temp_avg = 0
hum_avg = 0

#Check if there is internet connection
con_url = "www.google.com"
con_resouce = "/intl/en/policies/privacy/" 
test_con = httplib.HTTPConnection(con_url)
connection = 0

try:
    test_con.request("GET", con_resouce)
    response = test_con.getresponse()
except httplib.ResponseNotReady as e:
    print "Improper connection"
except socket.gaierror as e:
    print "Not connected"
else:
    connection = 1
    print "Connected"
test_con.close()

#If there is internet connection gets data from DB 
if connection == 1:
    #Getting info from config file
    def getConfigurations():
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        configurationFile = path + '/config.json'
        configurations = json.loads(open(configurationFile).read())
        return configurations

    #DB variables
    configurations = getConfigurations()
    host = configurations["mysql"][0]["host"]
    user = configurations["mysql"][0]["user"]
    password = configurations["mysql"][0]["password"]
    database = configurations["mysql"][0]["database"]

    #Tries to write from log to DB
    while True:
        db = MySQLdb.connect(host, user, password, database)
        cur = db.cursor()
        sql = "SELECT * FROM tempHum ORDER BY thID DESC LIMIT 2"
        
        try:
            print "SELECT 2 last rows from DB"
            cur.execute(sql)
            data = cur.fetchall()
            print "Done"
            #print data
    
        except:
            print "Error"
     
        cur.close()
        db.close()
        break
    
    temp1 = data[0][3]
    temp2 = data[1][3]
    hum1 = data[0][4]
    hum2 = data[1][4]

    print temp1
    print temp2
    print hum1
    print hum2

else:
    #Gets data from log
    with open ('logTempHum.txt') as foo:
        lineCount = len(foo.readlines())
        
    print "Linecount:", lineCount
    datalines = []
    #Gets data from log
    with open ('logTempHum.txt', "r") as fp:
        for i in fp.readlines():
            i = i.strip()
            tmp = i.split(",")
            datalines.append((tmp[0], tmp[1], tmp[2], tmp[3]))

    temp1 = datalines[lineCount - 1][2]
    temp2 = datalines[lineCount - 2][2]
    hum1 = datalines[lineCount - 1][3]
    hum2 = datalines[lineCount - 2][3]

    print temp1
    print temp2
    print hum1
    print hum2

##Code for opening windows
temp_avg = (temp1 + temp2) / 2
hum_avg = (hum1 + hum2) / 2
temp_avg = round(temp_avg, 1)
hum_avg = round(hum_avg, 1) 

print "Avergage temp:", temp_avg
print "Average hum:", hum_avg

#Functions for window movement
def init():
      gpio.setmode(gpio.BCM)
      gpio.setup(6, gpio.OUT)
      gpio.setup(13, gpio.OUT)
      gpio.setup(19, gpio.OUT)
      gpio.setup(5, gpio.OUT)
      gpio.setup(21, gpio.OUT, initial = gpio.HIGH) ## relay for motor controller
 

def closeWin(tf):
      closeLock()
      init()

      #closing pins
      gpio.output(21, False) ## relay for motor controller
      gpio.output(19, False)
      gpio.output(13, True)
      time.sleep(tf)
      gpio.cleanup()

def openWin(tf):
      openLock()
      init()
      
      #opening pins
      gpio.output(21, False) ## relay for motor controller
      gpio.output(19, True)
      gpio.output(13, False)
      time.sleep(tf)
      
      gpio.cleanup()

def openLock():
      init()

      #rises totally closed position GH window
      gpio.output(21, False) ## relay for motor controller
      gpio.output(19, True)
      gpio.output(13, False)
      gpio.output(5, False)
      time.sleep(2)
      
      gpio.cleanup()
      print "open clip opened"
      time.sleep(2)

def closeLock():
     init()

     #rises totally open position GH window
     gpio.output(21, False) ## relay for motor controller
     gpio.output(19, False)
     gpio.output(13, True)
     gpio.output(6, False)
     time.sleep(2)

     gpio.cleanup()
     print "close clip opened"
     time.sleep(2)

try:
     if temp_avg > 26:
         print "Open window"
         openWin(3)
     else:
         print "Close window"
         closeWin(3)
        
except KeyboardInterrupt:
    print "Keyboard interrupt"

except:
    print "Other error occurred!"

finally:
    gpio.cleanup()
