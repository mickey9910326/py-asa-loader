import py_asa_loader
import serial

bin = py_asa_loader.parseHex('main.hex')

print(len(bin))
