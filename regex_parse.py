"""
Derived from https://github.com/darius/peglet/blob/master/examples/regex.py
"""

from functools import reduce
from peglet import Parser, join

def make_parser(maker):
    def empty():       return maker.empty
    def literal(char): return maker.literal(char)
    def dot():         return maker.anyone
    def chain(r, s):   return maker.chain(r, s)
    def either(r, s):  return maker.either(r, s)
    def star(r):       return maker.star(r)
    def plus(r):       return maker.plus(r)

    def optional(r):   return either(r, empty())
    if hasattr(maker, 'oneof'):
        oneof = maker.oneof
    else:
        def oneof(chars):  return reduce(either, map(literal, chars))

    parser = Parser(r"""
regex   = exp $

exp     = term [|] exp    either
        | term
        |                 empty

term    = factor term     chain
        | factor

factor  = primary [*]     star
        | primary [+]     plus
        | primary [?]     optional
        | primary

primary = \( exp \)
        | \[ charset \]   join oneof
        | [.]             dot
        | \\(.)           literal
        | ([^.()*+?|[\]]) literal

charset = char charset
        |
char    = \\(.)
        | ([^\]])
""",
                  join=join,
                  **locals())
    return lambda s: parser(s)[0]

class Struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Test

if globals().get('halp'):

    class Mk:
        empty = ['']

        def literal(self, char):
            return [char]

        def chain(self, r, s):
            return [ri + sj for ri in r for sj in s]

        def either(self, r, s):
            return r + s

    parse = make_parser(Mk())

## parse('(Chloe|Yvette), a( precocious)? (toddler|writer)')
#. ['Chloe, a precocious toddler', 'Chloe, a precocious writer', 'Chloe, a toddler', 'Chloe, a writer', 'Yvette, a precocious toddler', 'Yvette, a precocious writer', 'Yvette, a toddler', 'Yvette, a writer']
