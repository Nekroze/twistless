"""
Twistless executor.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from functools import wraps
from twisted.internet import task
import stackless as sl


def Twistless(*args):
    """
    Wraps the entry point function, this function should setup and run a
    twisted reactor.

    A twisted task will be created to constantly schedule other stackless
    tasklets as often as the timesched argument.
    """
    def _twistless(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            """
            Calls the wrapped function in a stackless tasklet and sets up a
            looping twisted task to pump the schedueler.
            """
            @wraps(func)
            def execute():
                """
                Execute the entry point and create a looping call.
                """
                from .utils import REACTASK
                REACTASK = sl.getcurrent()
                task.LoopingCall(sl.schedule).start(timesched)
                func(*args, **kwargs)
            sl.tasklet(execute)()
            sl.run()
        return wrapped
    if len(args) == 1 and callable(args[0]):
        timesched = 0.01
        return _twistless(args[0])
    else:
        timesched = args[0] if len(args) >= 1 else 0.01
        return _twistless
