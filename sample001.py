#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys

#
# https://pythonhosted.org/pyserial/shortintro.html
#
import serial

def main():
    ser = serial.Serial(                \
        port = '/dev/ttyUSB0',          \
        baudrate = 9600,                \
        bytesize = serial.EIGHTBITS,    \
        parity = serial.PARITY_NONE,    \
        stopbits = serial.STOPBITS_ONE, \
        timeout = 0,        \
        write_timeout = 1,  \
        xonxoff = False,    \
        rtscts = True,      \
        dsrdtr = False,     \
        )
    ser.write(b'hello')
    return 0

if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
