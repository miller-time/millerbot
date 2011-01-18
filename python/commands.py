#!/usr/bin/python

import random

def action(msg):
    if msg.startswith('echo'):
        return msg[5:].strip()
    elif msg.lower() == 'quote':
        return quote()

def quote():
    f = open("quotes")
    st = f.read()
    f.close()
    quotes = st.split('\n')
    i = random.randint(0,len(quotes)-1)
    return quotes[i]
