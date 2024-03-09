#!/usr/bin/env python3
# coding=utf-8

import sys
import io

#
# https://pythonhosted.org/pyserial/shortintro.html
#
import serial

def main():
    ## ser = serial.serial_for_url(        \
    ##     url = '/dev/ttyUSB0',           \
    ser = serial.Serial(                \
        port = '/dev/ttyUSB0',          \
        baudrate = 9600,                \
        bytesize = serial.EIGHTBITS,    \
        parity = serial.PARITY_NONE,    \
        stopbits = serial.STOPBITS_ONE, \
        timeout = 10,        \
        write_timeout = 1,  \
        xonxoff = False,    \
        rtscts = True,      \
        dsrdtr = False,     \
        )
    ## sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser));

    print('CTS = %s'%str(ser.cts))
    print('RTS = %s'%str(ser.rts))

    ser.write(b'hello\r')

    ## line = sio.readline()
    line= ser.read()
    print(line)

    return 0

if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
