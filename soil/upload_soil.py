from sense import sense
from upload import upload


#Soil sensor 0x24
data = sense('Soil0x24', 200, 840, 0x24)
upload(data)