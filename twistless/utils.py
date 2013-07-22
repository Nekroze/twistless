"""
Twistless utilities, mainly decorators for enabling stackless functionality to
defereds.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from decorator import decorator
from twisted.internet import defer
from twisted.python import failure
import stackless as sl
REACTASK = None


def __filter(deferred):
    """
    Filter out the TaskletExit exception that messes with twisted causing
    unhandled defered errors.
    """
    if isinstance(deferred, failure.Failure):
        if isinstance(deferred.value, sl.TaskletExit):
            print("ignore taskletexit")
            return None
        return deferred
    return deferred


def __wrapper(deferred, func, *args, **kwargs):
    """
    Wraps a function in a defered for tasklet execution.
    """
    try:
        mabe = defer.maybeDeferred(func, *args, **kwargs)
        mabe.addCallback(__filter)
        mabe.addCallback(deferred.callback)
        mabe.addErrback(__filter)
    except sl.TaskletExit:
        pass
    except Exception as exc:
        print(exc, dir(exc))
        deferred.errback(exc)


def _block_on(deferred):
    """
    Block on the given deferred and setup a stackless channel as a callback to
    return later.
    """
    chan = sl.channel()
    deferred.addBoth(lambda x, y=chan: y.send(x))
    return chan.receive()


@decorator
def tasklet(func, *args, **kwargs):
    """
    Wrap a a function as a defered tasklet to be seperated from the main
    reactor execution when function called.
    """
    deferred = defer.Deferred()
    stasklet = sl.tasklet(__wrapper)
    stasklet(deferred, func, *args, **kwargs).run()
    return deferred


@decorator
def blocking(func, *args, **kwargs):
    """
    Wrap a function like the deferred decorator but call it as a blocking call
    to support synchronous calls in a tasklet outside of the reactor.

    WARNING: Currently does not function.
    """
    func2 = tasklet(func)
    deferred = func2(*args, **kwargs)
    if REACTASK != sl.getcurrent() and sl.getcurrent() != sl.getmain():
        return _block_on(deferred)
    raise RuntimeError("Cannot block in reactor task")
