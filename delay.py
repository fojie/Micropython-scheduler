# A time delay class for the micropython board. Based on the scheduler class. 24th Aug 2014
# Author: Peter Hinch
# V1.4 17 May 2016
# Used by Pushbutton library.
# This class implements the software equivalent of a retriggerable monostable. When first instantiated
# a delay object does nothing until it trigger method is called. It then enters a running state until
# the specified time elapses when it calls the optional callback function and stops running.
# A running delay may be retriggered by calling its trigger function: its time to run is now specified
# by the passed value.

# The usual caveats re microsheduler time periods applies: if you need millisecond accuracy
# (or better) use a hardware timer. Times can easily be -0 +20mS or more, depending on other threads

from usched import Sched, microsWhen, seconds, after, microsUntil, Timeout, wait


def _f(): pass
FunctionType = type(_f)                                     # Function or lambda


def _g():
    yield 1
ThreadType = type(_g)                                       # differs from type library. type(_g) != type(_g())


class _C:
    def _m(self): pass
MethodType = type(_C()._m)


class Delay(object):
    def __init__(self, objSched, callback=None, callback_args=()):
        self.objSched = objSched
        self.callback = callback
        self.callback_args = callback_args
        self._running = False

    def stop(self):
        self._running = False

    def trigger(self, duration):
        self.tstop = microsWhen(seconds(duration))          # Update end time
        if not self._running:                               # Start a thread which stops the
            self.objSched.add_thread(self.killer())         # delay after its period has elapsed
            self._running = True

    def running(self):
        return self._running

    def killer(self):
        to = Timeout(1)                                     # Initial value is arbitrary
        while not after(self.tstop):                        # Might have been retriggered
            yield to._ussetdelay(microsUntil(self.tstop))
        if self._running and self.callback is not None:
            self.callback(*self.callback_args)
        self._running = False


def _future(objSched, time_to_run, callback, callback_args):
    yield                                                   # No initialisation to do
    yield from wait(time_to_run)
    t = type(callback)
    if t is FunctionType or t is MethodType:
        callback(*callback_args)
    elif t is ThreadType:                                   # Generator function (thread)
        objSched.add_thread(callback(*callback_args))
    else:
        raise ValueError('future() received an invalid callback')


def future(objSched, time_to_run, callback, callback_args=()):
    objSched.add_thread(_future(objSched, time_to_run, callback, callback_args))
