#!/usr/bin/python

import random,re,math

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
        return "Syntax: !calc [expression]. Mathematical expression. Can include ceil,fabs,factorial,floor,exp,pow,sqrt,log,cos,sin,tan,degrees,radians,pi,e."
    if command == "echo":
        return "Syntax: !echo [message]. Stupid echo command."
    elif command == "quote":
        return "Syntax: !quote. Display a random quote from someone famous."
    elif command == "addquote":
        return "Syntax: !addquote [quote]. Request a quote be added."
    elif command == "join":
        return "Syntax: !join [channel] [channel key]"
    elif command == "?":
        return "Syntax: [question]? Shake the magic eightball..."
    else:
        return "Available commands: !calc !echo !quote !addquote !join !halp. Type !halp [command] for more info"

def calc(expr):
    print("Attempting to parse %s" % expr)
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
            print("Found constant %s" % const)
            return calc(match.group(1) + str(eval('math.' + const)) + match.group(2))
    for func in available_funcs:
        match = re.search(r'(.*?)' + func + r'\((.+?)\)(.*)', expr)
        if match:
            print("Found function %s" % func)
            eval_expr = 'math.' + func + '(' + match.group(2) + ')'
            return calc(match.group(1) + str(eval(eval_expr)) + match.group(3))
    match = re.search(r'[a-zA-Z_]',expr)
    if match:
        return "Invalid characters detected in expression."
    else:
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
