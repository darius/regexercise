"""
Fill in this stub.
"""

def search(re, chars):
    """Given a regular expression and an iterator of chars, return True if
    re matches some prefix of ''.join(chars); but only consume chars
    up to the end of the match."""
    raise NotImplementedError

# Regular-expression constructors; the re above is built by these.
# Feel free to change these definitions if it helps.
def literal(char):    return ('literal', char, None)
def chain(re1, re2):  return ('chain', re1, re2)
def either(re1, re2): return ('either', re1, re2)
def star(re):         return ('star', re, None)
