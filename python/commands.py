#!/usr/bin/python

import random

def action(user,chan,msg):
    # simple commands
    if msg.startswith('echo'):
        if chan[0] != '#':    # whispered
            return (user,msg[5:].strip())
        else:                 # said in channel
            return (chan,msg[5:].strip())
    elif msg.lower() == 'quote':
        return (chan,quote())
    elif msg.lower().startswith('halp'):
        return (chan,halp(msg[4:].strip()))
    elif msg.startswith("calc"):
        return (chan,calc(msg[4:].strip()))
    # admin commands
    elif msg.startswith("send") and user == "millertime":
        return parse_send(msg)
    elif msg.startswith("send"):
        return (chan,user + ": You don't have permission to do that.")
    elif msg.endswith("?"):
        return (chan,eightball())

def parse_send(msg):
    """Simple parser to split a channel name from a message"""
    msgList = msg.split(' ')
    channel = msgList[1]
    message = ' '.join(msgList[2:])
    return channel,message
    
def halp(command):
    if command == "calc":
        return "Syntax: !calc [expression]"
    if command == "echo":
        return "Syntax: !echo [message]"
    elif command == "quote":
        return "Syntax: !quote"
    elif command == "addquote":
        return "Syntax: !addquote [quote]"
    elif command == "join":
        return "Syntax: !join [channel] [channel key]"
    elif command == "?":
        return "Syntax: [question]?"
    else:
        return "Available commands: !echo !quote !addquote !join !halp"

def calc(expr):
    return str(eval(expr))

def quote():
    f = open("quotes")
    st = f.read()
    f.close()
    quotes = st.split('\n')
    i = random.randint(0,len(quotes)-1)
    return quotes[i]

def eightball():
    predictions = [ "As I see it, yes",
                    "It is certain",
                    "It is decidedly so",
                    "Most likely",
                    "Outlook good",
                    "Signs point to yes",
                    "Without a doubt",
                    "Yes",
                    "Yes - definitely",
                    "You may rely on it",
                    "Reply hazy, try again",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate and ask again",
                    "Don't count on it",
                    "My reply is no",
                    "My sources say no",
                    "Outlook not so good",
                    "Very doubtful"]
    return random.choice(predictions) + "."
