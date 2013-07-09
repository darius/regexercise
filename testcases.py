"""
Tests for the exercises.

I'll assume you supply functions named problem1(), problem2(),...
"""

def check1(problem1):

    def case1(pattern, string, remainder):
        check_patterns(pattern.split('|'), string, remainder)

    def check_patterns(patterns, string, remainder):
        stream = iter(string)
        result = problem1(patterns, stream)
        if remainder is None:
            assert result is None
            for ch in stream:
                assert False, "Stream should be exhausted"
        else:
            assert result is not None
            assert remainder == ''.join(stream)

    check_patterns([], '', None)
    check_patterns([], 'wheee', None)
    case1('', 'wheee', 'wheee')
    case1('X', 'wheee', None)
    case1('X', 'X', '')
    case1('X', 'wheXXXee', 'Xee')
    case1('X', 'yX', '')
    case1('X|X', 'yX', '')
    case1('X|YY', 'YX', '')
    case1(r'rat|cat', 'a cat is fat', ' is fat')
