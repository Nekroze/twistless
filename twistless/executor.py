"""
Twistless executor.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

def twistless(entrypoint, timesched=0.01):
    """
    Call the entry point function, this function should setup and run a twisted
    reactor.

    A twisted task will be created to constantly schedule other stackless
    tasklets as often as the timesched argument.
    """
    def execute():
        """
        Execute the entry point and create a looping call.
        """
        reactask = sl.getcurrent()
        task.LoopingCall(sl.schedule).start(timesched)
        entrypoint()
    sl.tasklet(execute).run()
    sl.run()
