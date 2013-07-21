"""
Twistless executor.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from functools import wraps


class Twistless(object):
    """
    Wraps the entry point function, this function should setup and run a
    twisted reactor.

    A twisted task will be created to constantly schedule other stackless
    tasklets as often as the timesched argument.
    """
    def __init__(self, timesched=0.01):
        self.timesched = timesched

    def __call__(self, func):
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
                task.LoopingCall(sl.schedule).start(self.timesched)
                func()
            sl.tasklet(execute).run()
            sl.run()
        return wrapped
