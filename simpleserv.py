"""
This example is based off of the echo server example from twisted matrix
documentation.

The original client will work fine and can be found here
http://twistedmatrix.com/documents/13.1.0/core/examples/simpleclient.py
"""
import twistless
import time
from stackless import schedule
from twisted.internet import reactor, protocol


@twistless.deferred
def async():
    """A deferred executed in another tasklet."""
    #Schedule this function to be continued at a later time.
    schedule()
    #Do something lengthy
    time.sleep(5)
    print("Tasklets!")


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        """
        As soon as any data is received, write it back ASAP. But first setup a
        function to be called when there is time for it.
        """
        #call the async deferred function in another tasklet
        #The server will echo a response and then return to the tasklet
        #schedule which has the async method waiting to be returned to.
        async()
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
