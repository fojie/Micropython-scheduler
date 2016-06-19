# instrument.py Demo of instrumenting code via the usched module's timer functions
# Author: Peter Hinch
# Copyright Peter Hinch 2016 Released under the MIT license

import pyb
from usched import Sched


# Run on MicroPython board bare hardware
# THREADS:

def instrument(objSched=None, interval=0.1, duration=10):
    if interval <= 0 or interval > duration:
        raise ValueError('Arguments are invalid')
    count = duration // interval
    max_overrun = 0
    while count:
        count -= 1
        result = yield interval
        max_overrun = max(max_overrun, result[2])
    print('Maximum timer overrun = {} us'.format(max_overrun))
    if objSched is not None:
        objSched.stop()


def thr_instrument(objSch, lstResult):
    yield                                       # Don't measure initialisation phase (README.md)
    while True:
        start = pyb.micros()                    # More typically we'd measure our own code
        yield                                   # but here we're measuring yield delays
        lstResult[0] = max(lstResult[0], pyb.elapsed_micros(start))
        lstResult[1] += 1


def robin(text):
    while True:
        print(text)
        yield


# USER TEST PROGRAM
def toggle(objLED, time):
    while True:
        yield
        objLED.toggle()


def test(duration):
    assert duration >= 1, 'Duration must be at least one second'
    print('Running test for {} seconds'.format(duration))
    objSched = Sched()
    leds = [pyb.LED(x) for x in range(1, 5)]                # Initialise all four on board LED's
    for x in range(4):                                      # Create a thread instance for each LED
        objSched.add_thread(toggle(leds[x], 0.2 + x / 2))
    # objSched.add_thread(robin("Thread 1"))                # Instantiate a few threads
    # objSched.add_thread(robin("Thread 2"))
    # objSched.add_thread(robin("Thread 3"))
    lstResult = [0, 0]
    objSched.add_thread(thr_instrument(objSched, lstResult))
    objSched.add_thread(instrument(objSched, 0.1, duration))
    objSched.run()
    print("Maximum roundrobin yield delay was {:1.1f} ms".format(lstResult[0] / 1000.0))
    print("Thread thr_instrument was executed {:1d} times in {:1d} seconds {:1d} Hz"
          .format(lstResult[1], duration, lstResult[1] // duration))

test(2)

