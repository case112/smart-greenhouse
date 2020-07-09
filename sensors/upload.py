import logging
import time
from insert import insert

logging.basicConfig(
    filename='sensors.log',
    format='\n[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def upload(data):

    counter = 0

    while counter < 5:
        try:
            insert(data)
            counter += 6

        except RuntimeError as error:
            print(error.args[0])
            logging.error('RuntimeError@upload:', exc_info=error)

        time.sleep(2.0)
        counter += 1
