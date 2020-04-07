from sense import sense
from upload import upload


#Soil sensor 0x24
data = sense('Soil0x24', 245, 655, 0x26)
upload(data)