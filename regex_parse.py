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
    def both(r, s):    return maker.both(r, s)

    def optional(r):   return either(r, empty())

    if not hasattr(maker, 'star') and not hasattr(maker, 'plus'):
        def star(r): raise Exception("No star() or star() constructor supplied")
        def plus(r): raise Exception("No plus() or star() constructor supplied")
    else:
        if hasattr(maker, 'star'):
            star = maker.star
        else:
            def star(r): return optional(plus(r))
        if hasattr(maker, 'plus'):
            plus = maker.plus
        else:
            def plus(r): return chain(r, star(r))

    if hasattr(maker, 'oneof'):
        oneof = maker.oneof
    else:
        def oneof(chars): return reduce(either, map(literal, chars))

    parser = Parser(r"""
regex   = exp $

exp     = term [|] exp    either
        | term & exp      both
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
