from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("hello, world!")

    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print "connection lost"


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


def main():
    f = EchoFactory()
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
