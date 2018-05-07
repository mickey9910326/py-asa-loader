'''##############################
#   Date     :  2017.11.29      #
#   Author   :  Wang Liang      #
#   Location :  NCU MVMC Lab    #
#   Version  :  v1.1            #
##############################'''

import serial
import serial.tools.list_ports
import re,os.path
from time import time,sleep


def read_hex(pos):
    buff = ''
    write_buff = b''
    with open(pos, 'r') as fp:
        for line in fp.readlines():
            buff = line[9:-3]
            write_buff += bytes.fromhex(buff)
    return write_buff

def Connect_RS232():

    #封包格式 : FC FC FC FC 01 + 2bytes(bytes數) + data + 1bytes(checksum)
    start = b'\xFC\xFC\xFC\xFA\x01\x00\x04\x74\x65\x73\x74\xC0'
    Connect_Check  = b'\xfc\xfc\xfc\xfb\x01\x00\x04OK!!\xdc'
    Package_normal  = b'\xFC\xFC\xFC\xFC\x01\x01\x00'
    Package_lastone = b'\xFC\xFC\xFC\xFC\x01'
    Package_End = b'\xFC\xFC\xFC\xFC\x01\x00\x00\x00'
    Return_m128 = b'\xFC\xFC\xFC\xFD\x01\x00\x04\x4F\x4B\x21\x21\xDC'

    coms = serial.tools.list_ports.comports()
    COM_port_list = []
    for i in coms:
        COM_port_list.append(re.findall('COM[0-9]',str(i))[0])
    print(COM_port_list)

    if len(COM_port_list) > 0:
        with serial.Serial(COM_port_list[0], baudrate=115200, timeout=1) as ser:
            t1 = time()
            write_buffer = b''
            write_pack = b''
            ser.write(start)

            while 1:
                ser.write(start)
                get_data = ser.readline()

                if get_data == Connect_Check:
                    print('---連線成功---')

                    pos = openfiledialog()

                    if pos == '':
                        return ' 沒有選擇到檔案! 請按下reset鈕'

                    write_buffer = read_hex(pos)   #讀取hex檔
                    fre = int(len(write_buffer)/256)    #做幾次

                    if int(len(write_buffer))%256 != 0:  #有餘數再加一次
                        fre += 1


                    t2 = time() #計算燒入時間
                    for number in range(0,fre):  #開始寫入
                        print('  [燒入中] 共{}包，現在第{:>2}包  '.format(fre,number+1),end="")
                        print('')
                        '''
                        for g in range(number+1):
                            print('{:>2} '.format(g+1),end='')
                        for g in range(fre-number-1):
                            print('__ ',end='')


                        '''
                        check_sum = 0
                        bytes_count = 0

                        if number<(fre-1):
                            for i in range((number)*256,(number+1)*256):
                                check_sum += write_buffer[i]
                                bytes_count += 1
                        else:
                            for i in range((number)*256,len(write_buffer)):
                                check_sum += write_buffer[i]
                                bytes_count += 1

                        check_sum = check_sum & (255)


                        temp = str(hex(check_sum)).split('x')[1]
                        #print(temp)

                        if check_sum <= 15: #單byte好像要兩個英文
                            temp = '0'+ temp

                        if number < (fre-1):   #普通封包
                            write_pack = Package_normal + write_buffer[(number)*256:(number+1)*256] + bytes.fromhex(temp)

                        else:   #最後一包
                            #bytes
                            if bytes_count <= 15:
                                bytes_count = str(hex(bytes_count)).split('x')[1]
                                bytes_count = '000' + bytes_count
                            elif bytes_count <= 255:
                                bytes_count = str(hex(bytes_count)).split('x')[1]
                                bytes_count = '00' + bytes_count
                            elif bytes_count <= 4095:
                                bytes_count = str(hex(bytes_count)).split('x')[1]
                                bytes_count = '0' + bytes_count
                            #print(bytes_count)
                            write_pack = Package_lastone + bytes.fromhex(bytes_count) + write_buffer[number*256:] + bytes.fromhex(temp)

                        ser.write(write_pack)
                        if (time()-t2) >0.5:
                            #ser.close()
                            return "燒入過程有誤!!"

                        t2 =  time()
                        #print(write_pack)
                        sleep(0.02)

                    while 1:
                        ser.write(Package_End)
                        get_data = ser.readline()
                        if get_data == Return_m128 :
                            t3 = time() #計算燒入時間
                            ser.close()
                            return '-----------------------------------------------\n 燒入成功了!\n  共花了{}秒'.format(t3-t2)
                else:
                    print(get_data)
                if (time()-t1) >3:
                    ser.close()
                    return "Error, 連線時間超過5秒, 請檢查檔位"
    else:
        return "沒有USB裝置"



def openfiledialog():

    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()


    fullpath_pbm,fname = os.path.split(__file__)
    #print(fullpath_pbm)

    fullpath = ''
    if os.path.isfile(fullpath_pbm + '\pos.txt') == True:
        #print('1')
        with open(fullpath_pbm + '\pos.txt', 'r', encoding = 'UTF-8-sig') as fp:
            fullpath = fp.readline()

    else:
        with open(fullpath_pbm + '\pos.txt', 'w', encoding = 'UTF-8-sig') as fp:
            #print('2')
            fullpath = fullpath_pbm
            fp.write(fullpath_pbm)

    file_path = filedialog.askopenfilename(filetypes=[("Hex files","*.hex")], initialdir=fullpath)
    #print(type(file_path))

    if file_path != "":
        with open(fullpath_pbm + '\pos.txt', 'w', encoding = 'UTF-8-sig') as fp:
            fp.write(file_path)
    else:
        with open(fullpath_pbm + '\pos.txt', 'w', encoding = 'UTF-8-sig') as fp:
            fp.write(fullpath_pbm)

    return file_path


if __name__ == "__main__":

    print(Connect_RS232())
    sleep(1)
