#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import glob
import serial
import argparse
from time import time,sleep
import py_asa_loader

def read_hex(pos):
    buff = ''
    write_buff = b''
    with open(pos, 'r') as fp:
        for line in fp.readlines():
            buff = line[9:-3]
            write_buff += bytes.fromhex(buff)
    return write_buff

def test():
    print("hello world!")


# def __main__():
if __name__ == '__main__':
    test()

    parser = argparse.ArgumentParser(description='Load program to ASA series board.')
    parser.add_argument('--hex',
                        dest='hexfile', action ='store', type = str,
                        help='assign hex file to be load')
    parser.add_argument('-p', '--port',
                        dest='portnum', action ='store', type = str,
                        help='assign the port to load')

    args = parser.parse_args()

    print(args.hexfile)
    print(args.portnum)

    l = py_asa_loader.Loader(args.portnum, args.hexfile)
    l.start()
    # print(l.checkDevice())
    # print(l.loadData())
    # print(l.lastData())
