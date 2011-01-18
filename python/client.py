#!/usr/bin/python

from twisted.words.protocols import irc
from twisted.internet import protocol

class MillerBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        if msg.startswith(self.nickname):
            msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
            prefix = "%s: " % (user.split('!', 1)[0], )
        else:
            prefix = ''
        if prefix:
            self.msg(self.factory.channel, prefix + msg)

class MillerBotFactory(protocol.ClientFactory):
    protocol = MillerBot

    def __init__(self, channel, nickname):
        self.channel=channel
        self.nickname=nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
