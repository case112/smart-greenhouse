from sense_soil import sense_soil
from upload import upload


#Soil sensor 0x24
data = sense_soil('Soil0x24', 200, 840, 0x24)
upload(data)