import time
from datetime import datetime

def get_data():
    data_list = []
    now = datetime.now()
    data_list.append('Sensor4')
    data_list.append(12.56)
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(5)
    return data_list
