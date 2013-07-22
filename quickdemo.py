from twistless import twistless
from twisted.internet import reactor


@twistless
def entry():
    reactor.run()


if __name__ == "__main__":
    entry()
