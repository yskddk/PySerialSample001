#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import csv
import serial
import serial.tools.list_ports



# This line is required for all related files.
#   https://docs.python.org/ja/3/howto/logging.html
#   https://qiita.com/amedama/items/b856b2f30c2f38665701
#   https://qiita.com/shinsa82/items/a0778fbd127012c93577
from logging import (basicConfig, getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL)

# This line is required in the program main file only.
basicConfig(level = DEBUG)
#basicConfig(level = INFO)
#basicConfig(level = WARNING)   # as default
#basicConfig(level = ERROR)
#basicConfig(level = CRITICAL)

# This line is required for all related files.
# After this, we can use those logging functions:
#   LOG_.debug()
#   LOG_.info()
#   LOG_.warning()
#   LOG_.error()
#   LOG_.critical()
#   LOG_.exception()
LOG_ = getLogger(__name__)



def open_com(com_fpath_):
    """
    Open the specified COM port.

    Parameter
    ---------
    com_fpath_ : string
        Full-path of the COM port character device file.

    Return
    ------
    serial_obj : list
        serial.Serial object.
    """
    ser = serial.Serial(                \
        port = com_fpath_,              \
        baudrate = 9600,                \
        bytesize = serial.EIGHTBITS,    \
        parity = serial.PARITY_NONE,    \
        stopbits = serial.STOPBITS_ONE, \
        write_timeout = 0.5,            \
        timeout = 0.5,                  \
        xonxoff = False,                \
        rtscts = True,                  \
        dsrdtr = False,                 \
        )
    return ser



def read_csv(csv_fpath_):
    """
    Get the (x,y) position data from the CSV file and return as list.

    Parameter
    ---------
    csv_fpath_ : string
        Full-path of the CSV file.

    Return
    ------
    read_data : list
        List object of (x,y) position data obtained from the CSV file.
    """

    read_data = []
    with open(csv_fpath_, encoding = 'utf-8', newline = '') as f_:
        csv_ = csv.reader(f_)
        read_data = [row_ for row_ in csv_]

    return read_data



def readline_CR(ser_):
    """
    This version of the readline() treats newline as CR.
    Referenced to https://stackoverflow.com/questions/16470903/ .

    Parameter
    ---------
    ser_ : serial.Serial object
        Serial package's class object.

    Return
    ------
    read_line : bytearray
        Received 1 line of data as a bytes object with CR at the end.
    """
    CR__ = b'\r'
    read_line = bytearray()

    while True:
        c = ser_.read(1)
        if not c:
            # no data
            read_line = bytearray() #clear
            break

        read_line += c
        if c == CR__:
            break

    return bytes(read_line)

def main():

    # List the COM ports
    #   https://pyserial.readthedocs.io/en/latest/tools.html#serial.tools.list_ports.ListPortInfo
    com_ports = serial.tools.list_ports.comports()
    if (0 == len(com_ports)):
        print('No serial ports found.')
        return 0

    LOG_.debug('{} COM ports found'.format(len(com_ports)))
    ## for com in com_ports:
    ##     LOG_.debug(com.device)

    serialObj = open_com(com_ports[0].device)

    # Get the (x,y) position data
    positions = read_csv('sample003.csv')
    LOG_.debug('{} positions found'.format(len(positions)))

    i = 0
    for item in positions:
        val_ = input('HIT ENTER KEY TO NEXT..')
        if '#' == item[0]:
            LOG_.debug('[{}] comment: {}'.format(i, item[1]))
        else:
            LOG_.debug('[{}] position: ({}, {})'.format(i, item[0], item[1]))
        i += 1

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
