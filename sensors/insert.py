#echo DATABASE_URL=$(heroku config:get DATABASE_URL -a appname) > conf.txt
import logging
import psycopg2
import os
from decouple import config

logging.basicConfig(
    filename='sensors.log',
    format='\n[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def insert(data):

    sensor_name_id = data[0]
    temperature = data[1]
    humidity = data[2]
    moisture = data[3]
    created_at = data[4]

    # Read database connection url from .env
    DATABASE_URL = config('DATABASE_URL')

    postgres_insert_query = """
                            INSERT INTO data_sensor (
                                sensor_name_id,
                                temperature,
                                humidity,
                                moisture,
                                created_at
                            ) 
                            VALUES (
                                %s, %s, %s, %s, %s
                            )
                            """

    record_to_insert = (sensor_name_id, temperature, humidity, moisture, created_at)

    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        cur.execute(postgres_insert_query, record_to_insert)
        con.commit()
        print (sensor_name_id, " successfully inserted into table")
        
        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Could not connect')
        print('Cause: {}'.format(error))
        logging.error('Exeption@insert:', data[0], exc_info=error)

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Connection closed')