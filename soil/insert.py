#echo DATABASE_URL=$(heroku config:get DATABASE_URL -a appname) > conf.txt
import psycopg2
import os
from decouple import config

def insert(data):

    sensor = data[0]
    moisture_value = data[1]
    moisture = data[2]
    temperature = data[3]
    date = data[4]

    # Read database connection url from .env
    DATABASE_URL = config('DATABASE_URL')

    postgres_insert_query = """
                            INSERT INTO data_chirp (
                                sensor,
                                moisture_value,
                                moisture
                                temperature,
                                date
                            ) 
                            VALUES (
                                %s, %s, %s, %s, %s
                            )
                            """

    record_to_insert = (sensor, moisture_value, moisture, temperature, date)

    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        cur.execute(postgres_insert_query, record_to_insert)
        con.commit()
        print (sensor, " successfully inserted into table")
        
        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Could not connect')
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Connection closed')