def search(re, chars):
    raise NotImplementedError

def literal(char): return ('literal', char, None)
def chain(r, s):   return ('chain', r, s)
def either(r, s):  return ('either', r, s)
