"""
Fill in this stub.

In a functional, black-box sense, this is no different from star.py,
and the same tests are applied. But you're to compile the regexes 
into a representation that will make matching more efficient.
"""

def search(re, chars):
    """Given a regular expression and an iterator of chars, return True
    if re matches some substring of ''.join(chars); but only consume
    chars up to the end of the match."""
    raise NotImplementedError

# Regular-expression constructors; the re above is built by these.
# Feel free to change these definitions if it helps.
def literal(char):    return ('literal', char, None)
def chain(re1, re2):  return ('chain', re1, re2)
def either(re1, re2): return ('either', re1, re2)
def plus(re):         return ('plus', re, None)
def star(re):         return ('star', re, None)
