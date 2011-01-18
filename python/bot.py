#!/usr/bin/python

import re
from twisted.internet import reactor
from client import MillerBotFactory

class Bot:
    def __init__(self):
        self.host = 'irc.cat.pdx.edu'     # default
        self.port = 6667                  # default
        self.chan = 'millerbot-testing'   # default
        self.nick = 'millerbot'           # default
        f = open("config")
        st = f.read()
        f.close()
        match = re.search(r'HOST=(.+)\n', st)
        if match:
            self.host = match.group(1)
        match = re.search(r'PORT=(.+)\n', st)
        if match:
            self.port = int(match.group(1))
        match = re.search(r'CHANNEL=(.+)\n', st)
        if match:
            self.chan = match.group(1)
        match = re.search(r'NICK=(.+)\n', st)
        if match:
            self.nick = match.group(1)
        
    def go(self):
        reactor.connectTCP(self.host,self.port,MillerBotFactory('#'+self.chan,self.nick))
        reactor.run()
