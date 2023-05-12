from barcode import EAN13
from barcode.writer import ImageWriter
import random

with open('barcode.jpg', 'wb') as f:
    numero = random.randint(100000000000, 999999999999)
    numero = str(numero)
    EAN13(numero, writer=ImageWriter()).write(f)