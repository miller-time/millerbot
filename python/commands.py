#!/usr/bin/python

import random

def action(msg):
    if msg.startswith('echo'):
        return msg[5:].strip()
    elif msg.lower() == 'quote':
        return quote()
    elif msg.startswith('fight'):
        return fight()

def quote():
    f = open("quotes")
    st = f.read()
    f.close()
    quotes = st.split('\n')
    i = random.randint(0,len(quotes)-1)
    return quotes[i]

def fight():
    phrases = [
        'WhopBot is a pansie.',
        'WhopBot smells like day-old seafood.',
        'WhopBot only wishes he could stand a chance.',
        "WhopBot's insults are pathetic.",
        'WhopBot sits down to pee.',
        "WhopBot isn't even Y2K compatible",
        "WhopBot is overheating I think. Might wanna get that looked at.",
        "WhopBot does not impress anyone.",
        "WhopBot was purchased at the toilet store.",
        "WhopBot should save his breath...He'll need it to blow up his date.",
        "Calling WhopBot stupid is an insult to stupid people.",
        "WhopBot's parents are brother and sister.",
        "I think WhopBot eats paint chips...",
        ]
    i = random.randint(0,len(phrases)-1)
    return phrases[i]
