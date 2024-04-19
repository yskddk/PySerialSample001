#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import time
import gpiozero



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



g_btn_next_   = False
g_btn_prev_   = False
g_btn_reload_ = False



def btn_next_handler():
    LOG_.debug('next pushed')
    global g_btn_next_
    g_btn_next_ = True
    return
   


def btn_prev_handler():
    LOG_.debug('prev pushed')
    global g_btn_prev_
    g_btn_prev_ = True
    return



def btn_reload_handler():
    LOG_.debug('reload pushed')
    global g_btn_reload_
    g_btn_reload_ = True
    return



def main():
    # https://gpiozero.readthedocs.io/en/latest/recipes.html
    # pin #34, GND

    global g_btn_next_
    global g_btn_prev_
    global g_btn_reload_

    btn_next   = gpiozero.Button('GPIO13')  # pin #33
    btn_prev   = gpiozero.Button('GPIO19')  # pin #35
    btn_reload = gpiozero.Button('GPIO26')  # pin #37
    
    btn_next.when_pressed   = btn_next_handler
    btn_prev.when_pressed   = btn_prev_handler
    btn_reload.when_pressed = btn_reload_handler

    led_ind = gpiozero.LED('GPIO21')        # pin #40
    led_ind.on()

    i = 0
    while True:
        time.sleep(0.25);

        if g_btn_next_:
            eprint_('NEXT')
        
        if g_btn_prev_:
            eprint_('PREV')

        if g_btn_reload_:
            eprint_('RELOAD')

        g_btn_next_   = False
        g_btn_prev_   = False
        g_btn_reload_ = False

        i += 1
        if 1 == (i % 2):
            LOG_.debug('LED ON');
            led_ind.on()
        else:
            LOG_.debug('LED OFF');
            led_ind.off()

    return 0



if __name__ == '__main__':
    # execute only if run as a script
    sys.exit(main())
