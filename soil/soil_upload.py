import sys
import os
import MySQLdb
import json
import httplib
import socket

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

#Getting data from log file (saved there if no connection) line by line and adding it to tuple
log = []
with open("logSoil.txt", "r") as fp:
    for i in fp.readlines():
        i = i.strip()
        tmp = i.split(",")
        log.append((tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]))
print log

#If there is internet connection and there is data saved to log, uploads to DB 
if connection == 1 and log != []:
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

    #Tries to write from log to DB
    while True:
        db = MySQLdb.connect(host, user, password, database)
        cur = db.cursor()
        sql = "INSERT INTO soil (datetime,sensor,moisture,moistureperc,temp) VALUES (%s,%s,%s,%s,%s)"
        
        try:
            print "Writing to DB"
            cur.executemany(sql, log)
            db.commit()
            print "Done"
            #Deletes log file after successful DB entry
            with open("logSoil.txt", "w"):
                pass
     
        except:
            #Rollback if error
            db.rollback()
            print "Error"
     
        cur.close()
        db.close()
        break

else:
    print("Try again later")
