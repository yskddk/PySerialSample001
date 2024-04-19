#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import time
import csv
import serial
import serial.tools.list_ports



# https://stackoverflow.com/questions/5574702/how-do-i-print-to-stderr-in-python
def eprint_(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



# This line is required for all related files.
#   https://docs.python.org/ja/3/howto/logging.html
#   https://qiita.com/amedama/items/b856b2f30c2f38665701
#   https://qiita.com/shinsa82/items/a0778fbd127012c93577
from logging import (basicConfig, getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL)

# This line is required in the program main file only.
#basicConfig(level = DEBUG)
#basicConfig(level = INFO)
basicConfig(level = WARNING)   # as default
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



def open_com(com_fpath_):
    """
    Open the specified COM port.

    Parameter
    ---------
    com_fpath_ : string
        Full-path of the COM port character device file.

    Return
    ------
    serial_obj : serial.Serial
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



def send_command(ser_, cmd_):
    """
    Send command and wait response.

    Parameters
    ----------
    ser_ : serial.Serial
        serial.Serial object.
    cmd_ : bytes
        Command bytes.

    Return
    ------
    result : bool
        Happened error returns False, otherwize returns True.
    """
    LOG_.debug('dev={} cmd_={}'.format(ser_.port, cmd_))

    try:
        # send command
        ser_.write(cmd_)
        return True

    except:
        return False



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
    try:
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

    except:
        return CR__



def wait_for_axis_moving(ser_):
    """
    Wait for axises moving to stop.

    Parameters
    ----------
    ser_ : serial.Serial
        serial.Serial object.

    Return
    ------
    result : bool
        Happened error returns False, otherwize returns True.
    """
    try:
        while True:
            time.sleep(0.25)

            cmd = b'MOTIONAll?\r'
            send_command(ser_, cmd)
            rsp = readline_CR(ser_)

            flags = int(rsp.decode('ascii').replace('\r', ''))
            flags = (0x03 & flags)
            LOG_.debug('axis 0x0{}'.format(flags))
            if 0 == flags:
                return True

    except:
        return False



def main():
    # List the COM ports
    #   https://pyserial.readthedocs.io/en/latest/tools.html#serial.tools.list_ports.ListPortInfo
    com_ports = serial.tools.list_ports.comports()
    LOG_.debug('{} COM port(s) found'.format(len(com_ports)))
    if (0 == len(com_ports)):
        eprint_('No serial ports found.');
        return 0

    ## for cport in com_ports:
    ##     LOG_.debug('+++ {}'.format(cport.device))

    LOG_.debug('open {}'.format(com_ports[0].device))
    serialObj = open_com(com_ports[0].device)

    # Get the (x,y) position data
    positions = read_csv('sample004.csv')
    LOG_.debug('{} positions found'.format(len(positions)))

    LOG_.debug('polling *ESR? to enter REMOTE mode')
    cmd = b'*ESR?\r'
    send_command(serialObj, cmd)
    rsp = readline_CR(serialObj)
    LOG_.debug('cmd "{}" rsp "{}"'.format(      \
        cmd.decode('ascii').replace('\r', ''),  \
        rsp.decode('ascii').replace('\r', '')))
    time.sleep(0.25)

    i = 0
    for item in positions:
        if '#' == item[0]:
            eprint_('[{}] {}'.format(i, item[1]))
        else:
            eprint_('[{}] HIT ENTER KEY TO NEXT..'.format(i))
            dummy = input()
            LOG_.debug('[{}] position: ({}, {})'.format(i, item[0], item[1]))
            cmd = 'AXIsX:GOABSolute {}:AXIsY:GOABSolute {}\r'.format(item[0], item[1]).encode('ascii')
            send_command(serialObj, cmd);
            wait_for_axis_moving(serialObj)
            time.sleep(0.25)
        i += 1

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
