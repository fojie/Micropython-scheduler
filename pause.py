# roundrobin.py Runs three threads in round robin fashion. Stops after a duration via a timeout thread.
# Author: Peter Hinch
# Copyright Peter Hinch 2016 Released under the MIT license

import pyb
from usched import Sched


# Run on MicroPython board bare hardware
# THREADS:

def stop(fTim, objSch):                                     # Stop the scheduler after fTim seconds
    yield fTim
    objSch.stop()


def robin(text):
    while True:
        pyb.delay(100)
        print(text)
        yield


def pauser(objSched, thread):
    for _ in range(3):
        yield 1
        objSched.pause(thread)
        print('Thread 2 paused')
        yield 1
        objSched.resume(thread)
        print('thread 2 resumed')
    yield 1
    objSched.stop(thread)
    print('thread 2 killed')


# USER TEST PROGRAM

def test(duration=0):
    objSched = Sched()
    objSched.add_thread(robin("Thread 1"))
    th2 = objSched.add_thread(robin("Thread 2"))
    objSched.add_thread(robin("Thread 3"))
    objSched.add_thread(pauser(objSched, th2))
    if duration:
        objSched.add_thread(stop(duration, objSched))       # Kill after a period
    objSched.run()

test(10)

