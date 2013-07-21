"""
Twistless utilities, mainly decorators for enabling stackless functionality to
defereds.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from decorator import decorator
from twisted.internet import defer
import stackless as sl
REACTASK = None


def __filter(d):
    """
    Filter out the TaskletExit exception that messes with twisted causing
    unhandled defered errors.
    """
    if isinstance(d, failure.Failure):
        if isinstance(d.value, TaskletExit):
            print("ignore taskletexit")
            return None
        return d
    return d

def __wrapper(d, f, *args, **kwargs):
    """
    Wraps a function in a defered for tasklet execution.
    """
    try:
        rv = defer.maybeDeferred(f, *args, **kwargs)
        rv.addCallback(__filter)
        rv.addCallback(d.callback)
        rv.addErrback(__filter)
    except TaskletExit:
        pass
    except Exception, e:
        print(e, dir(e))
        d.errback(e)

def _block_on(d):
    """
    Block on the given deferred and setup a stackless channel as a callback to
    return later.
    """
    chan = sl.channel()
    d.addBoth( lambda x,y=chan: y.send(x) )
    return chan.receive()

@decorator
def deferred(f, *args, **kwargs):
    """
    Wrap a a function as a defered tasklet to be seperated from the main
    reactor execution when function called.
    """
    d = defer.Deferred()
    t = sl.tasklet(__wrapper)
    t(d, f, *args, **kwargs).run()
    return d

@decorator
def blocking(f, *args, **kwargs):
    """
    Wrap a function like the deferred decorator but call it as a blocking call
    to support synchronous calls in a tasklet outside of the reactor.
    """
    f2 = deferred(f)
    d = f2(*args, **kwargs)
    if REACTASK != sl.getcurrent() and sl.getcurrent() != sl.getmain():
        return _block_on(d)
    raise RuntimeError("Cannot block in reactor task")
