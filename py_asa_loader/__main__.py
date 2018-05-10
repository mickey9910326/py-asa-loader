import py_asa_loader
import argparse
import time
import sys

def argHandler():
    parser = argparse.ArgumentParser(description='Load program to ASA series board.')
    parser.add_argument('-H', '--hex',
                        dest='hexfile', action ='store', type = str,
                        help='assign hex file to be load')
    parser.add_argument('-p', '--port',
                        dest='portnum', action ='store', type = str,
                        help='assign the port to load')
    args = parser.parse_args()
    return args

def run():
    args = argHandler()
    bin = py_asa_loader.parseHex(args.hexfile)
    print('program size: {:0.2f} KB'.format(len(bin)/1024))

    loader = py_asa_loader.Loader(args.portnum ,args.hexfile)
    loader.start()

if __name__ == '__main__':
    run()
