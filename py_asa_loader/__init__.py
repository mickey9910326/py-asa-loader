from math import floor
import serial
from time import time,sleep
import progressbar

class Loader():
    def __init__(self, port, hexFilename):
        # 8,N,1 mode
        self.ser = serial.Serial(port=port, baudrate=115200, timeout=3)
        self.hexFilename = hexFilename
        self.bin = parseHex(hexFilename)

    def checkIsAsaDevice(self):
        # The 'chk' packet is used to check the device is ASA series board.
        # If is, board will response 'ack' packet.
        chk = b'\xFC\xFC\xFC\xFA\x01\x00\x04\x74\x65\x73\x74\xC0'
        ack = b'\xFC\xFC\xFC\xFB\x01\x00\x04OK!!\xdc'
        self.ser.write(chk)
        get_data = self.ser.readline(len(chk))
        if get_data == ack:
            return True
        else:
            return False

    def loadData(self, data):
        packet  = b'\xFC\xFC\xFC\xFC\x01'
        packet += len(data).to_bytes(2, byteorder='big')
        packet += data
        packet += (sum(data)%256).to_bytes(1, byteorder='big')
        self.ser.write(packet)

    def lastData(self):
        end = b'\xFC\xFC\xFC\xFC\x01\x00\x00\x00'
        ret = b'\xFC\xFC\xFC\xFD\x01\x00\x04OK!!\xdc'
        self.ser.write(end)
        get_data = self.ser.read(len(ret))
        if get_data == ret:
            return True
        else:
            return False

    def start(self):
        if self.checkIsAsaDevice() is False:
            raise Exception("checkIsAsaDevice fail!")

        times = floor(len(self.bin)/256)
        remain = len(self.bin)%256

        widgets=[
            ' [', progressbar.Timer(), '] ',
            progressbar.Bar(),
            progressbar.Counter(format='%(percentage)0.2f%%'),
        ]
        if remain is not 0:
            bar = progressbar.ProgressBar(max_value=times+1, widgets=widgets)
        else:
            bar = progressbar.ProgressBar(max_value=times, widgets=widgets)


        delay = 0.03
        for i in range(times):
            self.loadData(self.bin[i*256:(i+1)*256])
            bar.update(i)
            sleep(delay)

        i = i+1
        if remain is not 0:
            self.loadData(self.bin[i*256:-1])
            bar.update(i)
            sleep(delay)

        if self.lastData() is False:
            raise Exception("lastData fail!")

def parseHex(filename):
    bin = b''
    with open(filename, 'r') as hexfile:
        try:
            for line in hexfile.readlines():
                if line == ':00000001FF\n':
                    return bin
                elif line == ':00000001FF':
                    return bin
                if line[0] != ':':
                    raise Exception("Invalid hexfile!", filenane)
                bytes  = int(line[1:3], 16)
                addres = int(line[3:7], 16)
                type   = int(line[7:9], 16)
                bin += bytearray.fromhex(line[9:-3])
                # print('byte:'+str(bytes)+' a:'+str(addres)+' t:'+str(type)+' d:'+line[9:-3])
                # print(bytearray.fromhex(line[9:-3]))
        finally:
            hexfile.close()
