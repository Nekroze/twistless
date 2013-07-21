"""
This example is based off of the echo server example from twisted matrix
documentation.

The original client will work fine and can be found here
http://twistedmatrix.com/documents/13.1.0/core/examples/simpleclient.py
"""
import twistless
import stackless
from twisted.internet import reactor, protocol


@twistless.deferred
def async():
    """A deferred executed in another tasklet."""
    time.sleep(1)
    stackless.schedule()
    time.sleep(1)


@twistless.blocking
def block():
    """A blocking deferred tasklet."""
    return None


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        #call the async deferred function in another tasklet
        async()
        #call the blocking deferred
        #block()
        self.transport.write(data)


@twistless.Twistless
def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
