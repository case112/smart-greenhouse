#echo DATABASE_URL=$(heroku config:get DATABASE_URL -a appname) > .env
import psycopg2
import os
from decouple import Config, RepositoryEnv

def insert(data):
    
    DOTENV_FILE = '/home/pi/Desktop/smart-greenhouse/.env'
    env_config = Config(RepositoryEnv(DOTENV_FILE))

    sensor = data[0]
    state = data[1]
    date = data[2]

    # Read database connection url from .env
    DATABASE_URL = env_config.get('DATABASE_URL')

    postgres_insert_query = """
                            INSERT INTO data_windowstate (
                                sensor,
                                state,
                                date
                            ) 
                            VALUES (
                                %s, %s, %s
                            )
                            """

    record_to_insert = (sensor, state, date)

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
