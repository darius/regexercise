"""
Tests for the problems.
"""

import sys
import traceback

from regex_parse import make_parser
import hal_vm

all_problems = ('literals finite plus star plus_compiled star_compiled '
                'literals_hal both').split()
solutions = set(all_problems)

def main(argv):
    problems = argv[1:] or all_problems
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
        if name in solutions:
            url = "https://github.com/darius/regexercise_solutions/blob/master/%s.py" % name
            print("  Passed! See my solution at " + url)
        else:
            print("  Passed.")

def check(module, regex_string, string, remainder):
    parse = make_parser(module)
    check_search(module.search, regex_string, parse(regex_string),
                 string, remainder)

def check_search(search, pattern_string, pattern, string, remainder):
    correct_result = remainder is not None
    stream = iter(string)
    try:
        result = search(pattern, stream)
    except NotImplementedError:
        raise
    except:
        print_bounded_traceback()
        print(show_test_case(pattern_string, pattern, string, remainder, False))
        sys.exit(1)
    unconsumed = ''.join(stream)
    test_case = show_test_case(pattern_string, pattern, string, remainder,
                               True, result, unconsumed)
    if remainder is None:
        assert result is False, "Wrong result." + test_case
        assert not unconsumed, "The stream should be exhausted." + test_case
    else:
        assert result is True, "Wrong result." + test_case
        assert unconsumed == remainder, "Too much or too litle of the stream was consumed." + test_case

def show_test_case(pattern_string, pattern, string, remainder,
                   completed, result=None, unconsumed=None):
    correct_result = remainder is not None
    pairs = ()
    if pattern_string is not None:
        pairs += (("Regex:", pattern_string),)
    pairs += (("Pattern: ", pattern), ("Input:", string))
    if not completed:
        pairs += (("Result should be:", correct_result),)
    elif result is not correct_result:
        pairs += (("Result should be:", correct_result),
                  ("But result is:   ", result))
    if not completed:
        pairs += (("Remainder should be:", remainder),)
    elif unconsumed != (remainder or ''):
        pairs += (("Remainder should be:", remainder),
                  ("But remainder is:   ", unconsumed))
    return ''.join('\n %s %r' % pair for pair in pairs)

def print_bounded_traceback():
    lines = traceback.format_exc().splitlines()
    if 30 < len(lines):
        lines = lines[:15] + ['  [...]'] + lines[-15:]
    print('\n'.join(lines))

def check_literals(module):
    check_search(module.search, None, [], '', None)
    check_search(module.search, None, [], 'wheee', None)
    check_search(module.search, None, [''], 'wheee', 'wheee')
    check1_base(LiteralsRegexMaker(module.search))
    return "Literal patterns: all tests passed."

def check_literals_hal(module):
    # TODO other check_literals tests -- move 'em into regex tests
    check1_base(LiteralsRegexMaker(HalSearch(module.compile_pattern)))
    return "Literal patterns for HAL: all tests passed."

def HalSearch(compiler):
    def search(regex, chars):
        program = compiler(regex)
        return not not hal_vm.load_program(program, chars).run()
        # XXX make stream track getch
    return search

class LiteralsRegexMaker:
    def __init__(self, search):
        self.search = search
    empty = ['']
    def literal(self, char): return [char]
    def chain(self, r, s):   return [ri + sj for ri in r for sj in s]
    def either(self, r, s):  return r + s

def check1_base(module):
    check(module, r'X', '', None)
    check(module, r'X', 'wheee', None)
    check(module, r'X', 'X', '')
    check(module, r'X', 'XXXee', 'XXee')
    check(module, r'X', 'yX', None)
    check(module, r'X|X', 'yX', None)
    check(module, r'X|YY', 'YX', None)
    check(module, r'X|X', 'Xy', 'y')
    check(module, r'X|YY', 'XYY', 'YY')
    check(module, r'allo|a', 'alloha', 'lloha')
    check(module, r'ab', 'aab', None)
    check(module, r'ab', 'aba', 'a')
    check(module, r'rat|cat', 'cats are fat', 's are fat')
    check(module, r'XXX', 'XX', None)
    check(module, r'XXXY', 'XXXish?', None)
    check(module, r'XXXY', 'XXXY?', '?')
    check(module, r'bababy', 'bababyish', 'ish')
    check(module, r'bababy', 'babababyish', None)

def check_finite(module):
    check1_base(module)
    check(module, r'(0|1)'*20,
          '01100011000110001100 how are you?',
          ' how are you?')
    check(module, r'(0|1)'*20,
          '0110001100011000110 how are you?',
          None)
    check(module, r'(aa|a)'*2,
          'aaa b',
          'a b')
    check(module, r'(aa|a)'*40,
          'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa b',
          'aaaaa b')
    check(module, r'(aa|a)'*40,
          'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa b',
          None)
    return "Abstract data: all tests passed."

def check_plus(module):
    check_finite(module)
    check(module, r'A+', 'A', '')
    check(module, r'A+', 'AAA+, would do again.', 'AA+, would do again.')
    check(module, r'a[bc]+d', 'abdomen', 'omen')
    check(module, r'a[bc]+d', 'abcbdcb', 'cb')
    check(module, r'a[bc]+d', 'addomen', None)
    check(module, r'(cat|dog)+like', 'dogcatcatdogcatdogdogcatdogcatcatdogcatdogdogcatlikely', 'ly')
    return "Plus: all tests passed."

def check_plus_compiled(module):
    check_plus(module)
    return "Plus_compiled: all tests passed."

def check_star(module):
    check_plus(module)
    check(module, r'a*', '', '')
    check(module, r'ba*', '', None)
    check(module, r'ba*', 'bc', 'c')
    check(module, r'ab*c', 'abcd', 'd')
    check(module, r'ab*c', 'abd', None)
    check(module, r'yo(ab|c*a)*ba', 'yoaabcaccaabbaba', 'ba')
# These tests go beyond the official interface, but can help:
#    check(module, r'()*', '', '')
#    check(module, r'(()())*', '', '')
    check(module, r'a(b*)*d', 'ad attacks', ' attacks')
    check(module, r'a(b*)*d', 'abdomen', 'omen')
    return "Star: all tests passed."

def check_star_compiled(module):
    check_star(module)
    return "Star_compiled: all tests passed."

def check_both(module):
    check_star(module)
    check(module, r'a&b', 'a', None)
    check(module, r'a&a', 'a', '')
    # XXX lots more tests needed
    return "Both: all tests passed."

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
