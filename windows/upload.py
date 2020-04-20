import time
from insert import insert

def upload(data):

    counter = 0

    while counter < 5:
        try:
            insert(data)
            counter += 6

        except RuntimeError as error:
            print(error.args[0])

        time.sleep(2.0)
        counter += 1
