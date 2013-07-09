"""
Tests for the exercises.

I'll assume you supply functions named problem1(), problem2(),...
"""

def check1(patterns, string, remainder):
    stream = iter(string)
    result = problem1(patterns, stream)
    if remainder is None:
        assert result is None
        for ch in stream:
            assert False, "Stream should be exhausted"
    else:
        assert result is not None
        assert remainder == ''.join(stream)

check1([], '', None)
check1([], 'wheee', None)
check1([''], 'wheee', 'wheee')
check1(['X'], 'wheee', None)
check1(['X'], 'wheXXXee', 'Xee')
