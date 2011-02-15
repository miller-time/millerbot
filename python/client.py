#!/usr/bin/python

# MillerBot - client
# interface with irc commands
# Copyright 2011 Russell Miller

import re,sys
from OpenSSL import SSL
from twisted.words.protocols import irc
from twisted.internet import protocol,ssl
from commands import *

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
        otherChans = self.getOtherChans()
        for chan in otherChans:
            self.join(chan)

    def getOtherChans(self):
        chans = []
        f = open("config")
        for line in f:
            if line.startswith("CHANNELS="):
                chans.append(line[9:])
        f.close()
        return chans

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        """One level deeper than commands.py. More power to call other irc commands here"""
        if not user:
            return
        username = user.split('!', 1)[0]
        # catch ++ events in #music
        if channel == "#music":
            plusplusmagic(msg)
        # non-message commands
        if msg.startswith("!join"):
            self.join(msg[6:])
        elif msg.startswith("!leave") and username == "millertime":
            print("Leaving " + msg[7:])
            self.part(msg[7:])
        elif msg.startswith("!leave"):
            self.msg(channel,username + ": No. You're not the boss of me.")
        elif msg.startswith("!quit") and username == "millertime":
            print("Quitting")
            self.quit("Bye for now.")
        elif msg.startswith("!quit"):
            self.msg(channel,username + ": No. You're not the boss of me.")
        elif msg.startswith("!addquote"):
            self.msg("millertime","Add quote: " + msg[9:] + "?")
            self.msg(channel,username + ": Request for approval sent.")
        elif msg.startswith("!shows list"):
            showlist = list_shows()
            for show in showlist:
                self.msg(channel, show)
        # all other commands
        elif msg.startswith('!'):
            result = action(username,channel,msg[1:])
            if result:
                to_who,cmd = result
                log("[%s]*millerbot*: ->%s %s" % (channel,to_who,cmd))
                self.msg(to_who,cmd)
        log("[%s]%s: %s" % (channel,username,msg))

def log(message):
    """Append message to logfile"""
    f = open("millerbot.log", 'a')
    if f:
        f.write(message+ '\n')
        print(message)
        f.close()
    else:
        print("Logging error.")

def second(x):
    return x[1]

def plusplusmagic(msg):
    """Regex for ++ to catch band names."""
    match = re.findall(r'(\w+)\+\+', msg)   # catch words with ++
    match2 = re.findall(r'\((.+?)\)\+\+', msg)  # catch (spaced words) with ++
    if not match and not match2:
        return
    
    # otherwise there are ++'s in the message!
    bands = {}
    # load existing data                                                                           
    f = open("bandrankings")
    for line in f:
        n = line.split(' ')[0]  # number [space] bandname... n should be number
        name = line[len(n)+1:-1]  # length of numberstring.. chop that off and the space.
                                       # also chop \n off end
        bands[name] = int(n)
    f.close()

    # add normal ++ words to dict
    if len(match) > 1:
        for thing in match:
            if thing in bands:
                bands[thing] += 1
            else:
                bands[thing] = 1
    elif match:
        if match[0] in bands:
            bands[match[0]] += 1
        else:
            bands[match[0]] = 1

    if len(match2) > 1:
        for thing in match2:
            if thing in bands:
                bands[thing] += 1
            else:
                bands[thing] = 1
    elif match2:
        if match2[0] in bands:
            bands[match2[0]] += 1
        else:
            bands[match2[0]] = 1

    # ok all set, lets rewrite that file
    f = open("bandrankings",'w')
    output = ''
    for band,rank in sorted(bands.items(), key=second, reverse=True):
        output += str(rank) + ' ' + band + '\n'
    f.write(output)
    f.close()

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
