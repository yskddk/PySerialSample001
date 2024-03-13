#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import serial
import serial.tools.list_ports



def readline_cr_(ser_):
    """
    This version of the readline() treats newline as CR.
    It'll return bytes object.
    Referenced to https://stackoverflow.com/questions/16470903/ .
    """
    cr = b'\r'
    line = bytearray()

    while True:
        c_ = ser_.read(1)
        if not c_:
            line = bytearray() #clear
            break

        line += c_
        if c_ == cr:
            break

    return bytes(line)



def main():

    # Listup established serial ports on this PC
    # Referenced to https://pythonhosted.org/pyserial/shortintro.html

    found_ports_ = {}
    for i,port in enumerate(serial.tools.list_ports.comports()):
        print('Serial port found: [{}] {}'.format(i, port.device))
        found_ports_[str(i)] = port.device

    if (0 == len(found_ports_)):
        print('No serial ports found.')
        return 0

    port_name_ = found_ports_['0']
    print('Use the {}'.format(port_name_))

    ser = serial.Serial(                \
        port = port_name_,              \
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

    cmd = b'AXIsX:READY?\r'
    #cmd = b'*ESR?\r'
    print('CTS:{}/RTS:{}, before write, send {}'.format(ser.cts, ser.rts, cmd))

    ser.write(cmd)

    print('CTS:{}/RTS:{}, after write'.format(ser.cts, ser.rts))

    resp = readline_cr_(ser)
    rstr = resp.decode('ascii').strip('\r\n')

    if 0 == len(rstr):
        print('CTS:{}/RTS:{}, error'.format(ser.cts, ser.rts))
    else:
        print('CTS:{}/RTS:{}, received {}'.format(ser.cts, ser.rts, rstr))

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
