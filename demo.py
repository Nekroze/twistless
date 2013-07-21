from twistless import Twistless
from twisted.internet import reactor


@Twistless()
def entry():
    reactor.run()


if __name__ == "__main__":
    entry()
