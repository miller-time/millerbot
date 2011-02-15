#!/usr/bin/python

# MillerBot - commands
# Return strings back to client, depending on different command input
# Copyright 2011 Russell Miller

import random,re,math
from datetime import date

def action(user,chan,msg):
    """Direct the work flow around based on command given"""
    # simple commands
    if msg.lower() == 'quote':
        return (chan,quote())
    elif msg.startswith('WhopBot'):
        return (chan,'WhopBot: search !WhopBot')
    elif msg.lower().startswith('shows'):
        return (chan,shows(msg[5:].strip()))
    elif msg.lower().startswith('bands'):
        return (chan,bands(msg[5:].strip()))
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
    """Give help strings"""
    if command == "calc":
        return "Syntax: !calc [expression]. Mathematical expression. Can include ceil,fabs,factorial,floor,exp,pow,sqrt,log,cos,sin,tan,degrees,radians,pi,e."
    elif command == "shows":
        return "Syntax: !shows (list | add). Shows I want to go see. Feel free to add to the list. !halp shows add for more info."
    elif command == "shows add":
        return "Syntax: !shows add MMDDYYYY [Description]"
    elif command == "quote":
        return "Syntax: !quote. Display a random quote from someone famous."
    elif command == "addquote":
        return "Syntax: !addquote [quote]. Request a quote be added."
    elif command == "WhopBot":
        return "make WhopBot spam the channel"
    elif command == "join":
        return "Syntax: !join [channel] [channel key]"
    elif command == "?":
        return "Syntax: [question]? Shake the magic eightball..."
    else:
        return "Available commands: !calc !shows !quote !addquote !join !halp. Type !halp [command] for more info"

def calc(expr):
    """Do math"""
    available_funcs = [
        'ceil',
        'fabs',
        'factorial',
        'floor',
        'exp',
        'pow',
        'sqrt',
        'log',
        'cos',
        'sin',
        'tan',
        'degrees',
        'radians',
    ]
    available_constants = [
        'pi',
        'e',
    ]
    if not expr:
        return ''
    for const in available_constants:
        match = re.search(r'(.*?)' + const + r'(.*)', expr)
        if match:
            try:
                return calc(match.group(1) + str(eval('math.' + const)) + match.group(2))
            except SyntaxError:
                return "You typed something wrong."
    for func in available_funcs:
        match = re.search(r'(.*?)' + func + r'\((.+?)\)(.*)', expr)
        if match:
            eval_expr = 'math.' + func + '(' + match.group(2) + ')'
            try:
                return calc(match.group(1) + str(eval(eval_expr)) + match.group(3))
            except SyntaxError:
                return "You typed something wrong."
    match = re.search(r'[a-zA-Z_]',expr)
    if match:
        return "Invalid characters detected in expression."
    else:
        return str(eval(expr))

def quote():
    """Get a random quote"""
    f = open("quotes")
    st = f.read()
    f.close()
    quotes = st.split('\n')
    i = random.randint(0,len(quotes)-1)
    return quotes[i]

def shows(command):
    """Add a new show"""
    if command.startswith("add"):
        show_string = command[3:].strip()
        try:
            a = int(show_string[:8])
        except:
            return "Invalid date. Please use a 8-digit number for MMDDYYYY"
        show_date = date(int(show_string[4:8]),int(show_string[:2]),int(show_string[2:4]))
        shows_d = {}
        shows_d[show_date] = show_string + '\n'
        f = open("shows")
        for line in f:
            if len(line) >= 10:
                sd = date(int(line[4:8]),int(line[:2]),int(line[2:4]))
                shows_d[sd] = line
        f.close()
        new_data = []
        for show in sorted(shows_d.keys()):
            new_data.append(shows_d[show])
        f = open("shows",'w')
        f.write(''.join(new_data))
        f.close()
        return "New show added."
    else:
        return "More options coming soon."

def bands(command):
    """List most popular #music bands"""
    bands = []
    f = open("bandrankings")
    for line in f:
        if len(bands)>5:
            break
        n = line.split(' ')[0]
        bands.append(line[len(n)+1:-1])
    f.close()
    message = 'Top bands in this channel: ' + ', '.join(bands)
    return message

def list_shows():
    """List the current shows"""
    showlist = []
    f = open("shows")
    for line in f:
        if len(line) >= 10: # minimum length for date and 1 character description..
            d = date(int(line[4:8]),int(line[:2]),int(line[2:4]))
            showlist.append(d.strftime("%b %d, %Y") + ":" + line[8:-1])
    f.close()
    return showlist

def eightball():
    """Provide insight to questions"""
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
