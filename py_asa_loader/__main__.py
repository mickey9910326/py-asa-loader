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
    # print
    # setup toolbar
    toolbar_width = 30
    progress = 0
    progressStr = "[%s]" % (" " * toolbar_width) + "{:0.2f}".format(progress)
    sys.stdout.write(progressStr)
    sys.stdout.flush()
    sys.stdout.write("\r") # return to start of line, after '['

    for i in range(toolbar_width):
        progress = progress + 1
        time.sleep(0.1) # do real work here
        # update the bar
        progressStr = "[%s]" % (" " * toolbar_width) + "{:0.2f}".format(progress)
        sys.stdout.write(progressStr)
        sys.stdout.flush()

    sys.stdout.write("\n")

    # # TODO unsupport ed hex
    # # TODO serial
    # print()
    # print(args.portnum)
    #
    # l = py_asa_loader.Loader(args.portnum, args.hexfile)
    # l.start()


if __name__ == '__main__':
    run()
