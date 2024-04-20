#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import time
import gpiozero
import subprocess



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



g_btn_ldusb_  = False
g_btn_reload_ = False
g_btn_prev_   = False
g_btn_next_   = False



def btn_ldusb_handler():
    LOG_.debug('reload pushed')
    global g_btn_ldusb_
    g_btn_ldusb_ = True
    return



def btn_reload_handler():
    LOG_.debug('reload pushed')
    global g_btn_reload_
    g_btn_reload_ = True
    return



def btn_shdown_handler():
    LOG_.debug('shdown pushed')
    time.sleep(0.5);
    subprocess.check_call(['sudo', 'poweroff'])
    return



def btn_prev_handler():
    LOG_.debug('prev pushed')
    global g_btn_prev_
    g_btn_prev_ = True
    return



def btn_next_handler():
    LOG_.debug('next pushed')
    global g_btn_next_
    g_btn_next_ = True
    return
   


def switch_led(pattern_):

    if 'ON' == pattern_:
        LOG_.debug('led to {}'.format(pattern_))
        subprocess.check_call(['sudo', 'swled', 'ON'])

    elif 'OFF' == pattern_:
        LOG_.debug('led to {}'.format(pattern_))
        subprocess.check_call(['sudo', 'swled', 'OFF'])

    elif 'TIMER' == pattern_:
        LOG_.debug('led to {}'.format(pattern_))
        subprocess.check_call(['sudo', 'swled', 'TIMER'])

    elif 'HEARTBEAT' == pattern_:
        LOG_.debug('led to {}'.format(pattern_))
        subprocess.check_call(['sudo', 'swled', 'HEARTBEAT'])

    else:
        LOG_.debug('led not changed')

    return




def main():
    # https://gpiozero.readthedocs.io/en/latest/recipes.html
    # pin #34, GND

    global g_btn_ldusb_
    global g_btn_reload_
    global g_btn_prev_
    global g_btn_next_

    btn_shdown = gpiozero.Button('GPIO13')  # pin #33
    btn_ldusb  = gpiozero.Button('GPIO19')  # pin #35
    btn_reload = gpiozero.Button('GPIO26')  # pin #37
    btn_prev   = gpiozero.Button('GPIO20')  # pin #38
    btn_next   = gpiozero.Button('GPIO16')  # pin #36
    
    btn_shdown.when_pressed = btn_shdown_handler
    btn_ldusb.when_pressed  = btn_ldusb_handler
    btn_reload.when_pressed = btn_reload_handler
    btn_prev.when_pressed   = btn_prev_handler
    btn_next.when_pressed   = btn_next_handler

    led_ind = gpiozero.LED('GPIO21')        # pin #40
    led_ind.on()
    time.sleep(0.1)
    led_ind.off()
    time.sleep(0.1)
    led_ind.on()
    time.sleep(0.1)
    led_ind.off()
    time.sleep(0.1)

    switch_led('OFF')
    is_csv = False

    i = 0
    while True:
        time.sleep(0.1);

        if g_btn_ldusb_:
            eprint_('LDUSB')
            subprocess.check_call(['sudo', 'ldusb'])
            switch_led('OFF')
            is_csv = False

        if g_btn_reload_:
            eprint_('RELOAD')
            switch_led('ON')
            is_csv = True

        if g_btn_prev_:
            if is_csv:
                eprint_('PREV')
            else:
                switch_led('HEARTBEAT')

        if g_btn_next_:
            if is_csv:
                eprint_('NEXT')
            else:
                switch_led('HEARTBEAT')

        g_btn_ldusb_  = False
        g_btn_reload_ = False
        g_btn_prev_   = False
        g_btn_next_   = False

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
