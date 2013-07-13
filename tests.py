"""
Tests for the exercises.
Call check1(module_for_problem_1), check2(module_for_problem_2), ...
"""

from regex_parse import make_parser

def check_search(search, pattern, string, remainder):
    stream = iter(string)
    result = search(pattern, stream)
    unconsumed = ''.join(stream)
    test_case = ("Pattern: %r Input: %r Expected remainder: %r Actual remainder: %r"
                 % (pattern, string, remainder, unconsumed))
    if remainder is None:
        assert result is False, test_case
        assert not unconsumed, "Stream should be exhausted. " + test_case
    else:
        assert result is True, test_case
        assert unconsumed == remainder, test_case

def check(module, regex_string, string, remainder):
    parse = make_parser(module)
    check_search(module.search, parse(regex_string), string, remainder)

def check_literals(module):
    check_search(module.search, [], '', None)
    check_search(module.search, [], 'wheee', None)
    check_search(module.search, [''], 'wheee', 'wheee')
    check1_base(LiteralsRegexMaker(module.search))
    return "Literal patterns: all tests passed."

class LiteralsRegexMaker:
    def __init__(self, search):
        self.search = search
    empty = ['']
    def literal(self, char): return [char]
    def chain(self, r, s):   return [ri + sj for ri in r for sj in s]
    def either(self, r, s):  return r + s

def check1_base(module):
    check(module, r'X', 'wheee', None)
    check(module, r'X', 'X', '')
    check(module, r'X', 'wheXXXee', 'XXee')
    check(module, r'X', 'yX', '')
    check(module, r'X|X', 'yX', '')
    check(module, r'X|YY', 'YX', '')
    check(module, r'rat|cat', 'a cat is fat', ' is fat')
    check(module, r'XXX', 'XX', None)
    check(module, r'XXXY', 'r u XXXish or XXXY?', '?')

def check_abstract_data(module):
    check1_base(module)
    check(module, r'(0|1)'*20,
          'hello 01100011000110001100 how are you?',
          ' how are you?')
    check(module, r'(0|1)'*20,
          'hello 0110001100011000110 how are you?',
          None)
    check(module, r'(aa|a)'*40,
          'a aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa b',
          'aaaaa b')
    check(module, r'(aa|a)'*40,
          'a aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa b',
          None)
    return "Abstract data: all tests passed."

def check_repetition(module):
    check_abstract_data(module)
    check(module, r'A+', 'Rating AAA+, would do again.', 'AA+, would do again.')
    check(module, r'a[bc]+d', 'my abdomen', 'omen')
    check(module, r'a[bc]+d', 'abcbdcb', 'cb')
    check(module, r'a[bc]+d', 'my addomen', None)
    check(module, r'(cat|dog)+like', 'dogcatcatdogcatdogdogcatdogcatcatdogcatdogdogcatlikely', 'ly')
    return "Repetition: all tests passed."
