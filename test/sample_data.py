import time
from datetime import datetime

def get_data():
    data_list = []
    now = datetime.now()
    data_list.append('Sensor4')
    data_list.append(12.36)
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    return data_list
