from sample_data import get_data
from csv import writer

with open('data.csv', 'w', newline='') as f:
    data_writer = writer(f)
    while True:
        data = get_data()
        data_writer.writerow(data)
        print(data)