#!/usr/bin/python

import re,sys
from OpenSSL import SSL
from twisted.words.protocols import irc
from twisted.internet import protocol,ssl
from commands import *

def parse_send(msg):
    """Simple parser to split a channel name from a message"""
    print("Parsing msg: %s" % msg)
    msgList = msg.split(' ')
    channel = msgList[1]
    message = ' '.join(msgList[2:])
    return channel,message

class MillerBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def getPass(self):
        f = open("pw")
        pw = f.read()
        return pw

    def signedOn(self):
        self.join(self.factory.channel)
        print("self.factory.channel: %s" % self.factory.channel)
        print "Signed on as %s." % (self.nickname,)
        pw = self.getPass()
        self.msg("nickserv", "identify " + pw)
        print("/msg nickserv identify ****")

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        if msg.startswith('!'):
            msg = re.compile("![:,]* ?", re.I).sub('', msg)
            prefix = "%s: " % (user.split('!', 1)[0], )
        else:
            prefix = ''
        if prefix:
            if msg.startswith("join"):
                self.join(msg[5:])
            elif msg.startswith("addquote"):
                self.msg("millertime","Add quote: " + msg[9:] + "?")
            elif msg.startswith("send") and user.startswith("millertime!thatguy"):
                chan,message = parse_send(msg)
                self.msg(chan,message)
            elif msg.startswith("leave") and user.startswith("millertime!thatguy"):
                self.part(msg[6:])
            elif msg.startswith("quit") and user.startswith("millertime!thatguy"):
                self.quit("Bye for now.")
            elif msg:    
                cmd = action(msg)
                self.msg(channel, cmd)
        print msg

class MillerBotFactory(protocol.ClientFactory):
    protocol = MillerBot

    def __init__(self, channel, nickname):
        self.channel=channel
        self.nickname=nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s)" % (reason,)

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

class MillerBotContextFactory(ssl.ClientContextFactory):
    """A context factory for SSL clients."""
    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        return ctx
