# roundrobin.py Runs three threads in round robin fashion. Stops after a duration via a timeout thread.
# Author: Peter Hinch
# Copyright Peter Hinch 2016 Released under the MIT license

import pyb
from usched import Sched


# Run on MicroPython board bare hardware
# THREADS:

def stop(fTim, objSch):                                     # Stop the scheduler after fTim seconds
    yield fTim
    print('Stopping')
    objSch.stop()


def robin(text):
    while True:
        print(text)
        yield


# USER TEST PROGRAM

def test(duration=0):
    objSched = Sched(True, 1)                               # heartbeat on LED 1
    objSched.add_thread(robin("Thread 1"))
    objSched.add_thread(robin("Thread 2"))
    objSched.add_thread(robin("Thread 3"))
    if duration:
        objSched.add_thread(stop(duration, objSched))       # Kill after a period
    objSched.run()

test(5)
