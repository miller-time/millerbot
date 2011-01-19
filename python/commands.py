#!/usr/bin/python

import random

def action(msg):
    if msg.startswith('echo'):
        return msg[5:].strip()
    elif msg.lower() == 'quote':
        return quote()
    elif msg.lower() == 'help':
        return halp()
    elif msg.endswith("?"):
        return eightball()
    #elif msg.startswith('nag'):
        #return 'nagbot: say !nag'

def halp():
    return "Available commands: !echo !quote !help"

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
