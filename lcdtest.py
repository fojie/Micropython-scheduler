# lcdtest.py Demo/test program for MicroPython scheduler with attached LCD display
# Author: Peter Hinch
# Copyright Peter Hinch 2016 Released under the MIT license
# Display must use the Hitachi HD44780 controller. This demo assumes a 16*2 character unit.

# Folke Berglund: LCD configuration specified as LCD_NR_ROWS & LCD_NR_COLS

import pyb
from usched import Sched
from lcdthread import LCD, PINLIST                          # Library supporting Hitachi LCD module

LCD_NR_ROWS = const(4)
LCD_NR_COLS = const(20)

# HARDWARE
# Micropython board with LCD attached using the 4-wire data interface. See lcdthread.py for the
# default pinout. If yours is wired differently, declare a pinlist as per the details in lcdthread
# and instantiate the LCD using that list.


# THREADS:

def stop(fTim, objSch):                                     # Stop the scheduler after fTim seconds
    yield fTim
    objSch.stop()


def lcd_thread(mylcd):

    global LCD_NR_ROWS

    mylcd[0] = "MicroPython"
    while True:
        for row in range(1, LCD_NR_ROWS):
            mylcd[row] = "{:11d} us".format(pyb.micros())
            yield 1


# USER TEST PROGRAM
# Runs forever unless you pass a number of seconds

def test(duration=0):

    global LCD_NR_ROWS, LCD_NR_COLS

    if duration:
        print("Test LCD display for {:d} seconds".format(duration))
    objSched = Sched()
    lcd0 = LCD(PINLIST, objSched, cols=LCD_NR_COLS, rows=LCD_NR_ROWS)
    objSched.add_thread(lcd_thread(lcd0))
    if duration:
        objSched.add_thread(stop(duration, objSched))
    objSched.run()

test(20)

