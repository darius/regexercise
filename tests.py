"""
Tests for the problems.
"""

from regex_parse import make_parser

def main(argv):
    problems = argv[1:] or 'literals abstract_data repetition zero_or_more'.split()
    for problem in problems:
        test_problem(problem)
    return 0

def test_problem(name):
    module = __import__(name)
    check = globals()['check_'+name]
    print("Testing " + name + ".py: ")
    try:
        check(module)
    except NotImplementedError:
        print("  Nothing to test yet.")
    else:
        print("  Passed.")

def check_search(search, pattern, string, remainder):
    correct_result = remainder is not None
    stream = iter(string)
    result = search(pattern, stream)
    unconsumed = ''.join(stream)
    pairs = (("Pattern: ", pattern), ("Input:", string))
    if result is not correct_result:
        pairs += (("Result should be:", correct_result),
                  ("But result is:   ", result))
    if remainder != unconsumed:
        pairs += (("Remainder should be:", remainder),
                  ("But remainder is:   ", unconsumed))
    test_case = ''.join('\n %s %r' % pair for pair in pairs)
    if remainder is None:
        assert result is False, "Wrong result." + test_case
        assert not unconsumed, "The stream should be exhausted." + test_case
    else:
        assert result is True, "Wrong result." + test_case
        assert unconsumed == remainder, "Too much or too litle of the stream was consumed." + test_case

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
    check(module, r'hallo|a', 'hallo', 'llo')
    check(module, r'ab', 'aab', '')
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

def check_zero_or_more(module):
    check_repetition(module)
    check(module, r'a*', '', '')
    check(module, r'ab*c', 'an abba abcd', 'd')
    check(module, r'ab*c', 'an abba abd', None)
    check(module, r'yo(ab|c*a)*ba', 'a yoaabcaccaabbaba', 'ba')
    check(module, r'a(b*)*d', 'an ad attacks', ' attacks')
    check(module, r'a(b*)*d', 'an abdomen', 'omen')
    return "Zero or more: all tests passed."

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
