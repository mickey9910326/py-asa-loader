import py_asa_loader
import serial

bin = py_asa_loader.parseHex('main.hex')

print('program size: {:d} bytes'.format(len(bin)))
print('program size: {:0.2f} KB'.format(len(bin)/1024))
