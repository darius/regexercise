regexercise
===========

### Exercises in implementing regular-expression search

Let's say you know what a [regular
expression](http://en.wikipedia.org/wiki/Regular_expression) is,
you're a fairly experienced programmer, and you'd like to reach a
deeper understanding (or just have some fun) by writing a matcher for
them. These problems gradually work up to an implementation of
Thompson's algorithm, without telling you how to do it. Each has a
solution in a page or less of Python, using no especially advanced
Python features.

I'm confident my solutions are worth reading; on the other hand, I
have no idea whether this sequence of problems offered without telling
you the algorithm makes an effective way to learn; if you tackle this,
please tell me how it goes. ([Comment
here](https://github.com/darius/regexercise/issues) or email
withal@gmail.com.)

To start: `pip install peglet`, read the first problem below, edit
[literals.py](literals.py), then run `python tests.py` until it likes
your solution. The code is known to work in Python 2.7 and Python
3.2, and expected to work in 2.6 and up.

## The problems

**Literal patterns**: Given a list of strings, and a stream of
characters, read the stream and report as soon as one of the strings
occurs in it. (You don't have to report which one.) For example, in
Python we might ask

    >>> stream = iter('a cat is fat')
    >>> search(['rat', 'cat'], stream)  # Is 'rat' or 'cat' in the stream?
    True
    >>> ''.join(stream)  # The rest wasn't consumed, see:
    ' is fat'

Test your solution by defining it in a module [literals.py](literals.py). Then

    $ python tests.py

will check it. You can run just the literals tests via

    $ python tests.py literals

or

    >>> import tests, literals
    >>> tests.check_literals(literals)
    'Literal patterns: all tests passed.'

**Abstract data**: As before, but instead of a list of strings, we
take a restricted kind of regular expression. You can represent these
expressions however you like; define three constructors:

* `literal(character)` should represent a regex matching just that character.
* `either(regex1, regex2)` should match what either regex1 or
regex2 matches; i.e. it represents `regex1|regex2`.
* `chain(regex1, regex2)` matches a match of `regex1` followed
by a match of `regex2`; i.e. it represents `regex1 regex2`.

So you could encode the same pattern as before as

    >>> def sequence(regexes): return reduce(chain, regexes)
    >>> rat_or_cat = either(sequence(map(literal, 'rat')), sequence(map(literal, 'cat')))

and then, with your new search function, `search(rat_or_cat, stream)`
should produce the same result. Of course one way to solve this is,
just expand the pattern into a list of strings and leave `search`
unchanged. But this list of strings could get exponentially bigger
than the regular expression -- consider

    >>> bit = either(literal('0'), literal('1'))
    >>> ten_bits = sequence(10 * [bit])

`ten_bits`, a regex with 20 literals, would expand out to a list of
1024 strings; make it 30 bits and you'd get over a billion. (Also,
we're soon going to add in a repetition operator that'd make the set
of matching strings infinite.) So now you want to work with a more
tailored representation.

Put your code in [finite.py](finite.py) so [tests.py](tests.py)
knows where to find it.

**Repetition**: Now in [plus.py](plus.py) with one more
regex constructor:

* `plus(regex)` has matches consisting of 1 or more matches of `regex`
in sequence. (The Kleene plus: `(regex)+` in the usual notation.)

The following two problems could be tackled in either order.

**Matching nothing**: In [star.py](star.py) add the
`star` constructor, like `plus` but matching 0 or more. Getting the
matching to terminate may be tricky for patterns like
`star(star(regex))`.

**Compiling**: In [plus_compiled.py](plus_compiled.py) or
[star_compiled.py](star_compiled.py): Don't allocate any memory inside
the main matching loop. (Some languages would make satisfying the
letter of this requirement more painful than it's worth; so it's
enough if there's an obvious translation into an allocation-free loop
in a lower-level language.)

**Machine code for literal patterns**: In
[literals_hal.py](literals_hal.py). Take literal patterns, as in the
first problem, but before the start of matching compile them into a
machine-code program that'll do the matching. I've defined a simple
target machine for this, the [HAL 100](hal-100.md), since the IBM 7094
that Thompson used was kind of tricky and obscure.

**Machine code**: As above, but for regular expressions. You might
jump straight to this problem if you're confident and impatient.

**Bonus:** Add a `both(regex1, regex2)` constructor that matches when
both of its arguments match.

## General hints

For all these problems you can keep a set of states of some kind; in
the main loop you ask if any of the states is the matched state, and
if not, get the next character from the stream and update the
state-set according to it. For the first problem [here's
pseudocode](http://stackoverflow.com/a/846728/27024) (in the first
part of the answer; it assumes there's just one pattern string, but
generalizes easily).

What kind of states will work for the subsequent problems?
Essentially, regular expressions again: if a state represents a
regular expression r, and you get input character c, then the
[Brzozowski
derivative](http://blog.sigfpe.com/2005/05/derivatives-of-regular-expressions.html)
dr/dc is the next state. Thompson represents dr/dc as a set of 0 or
more possible next states. If r is `ax|ay` and c is `a`, then you
could get either one next state, `x|y`, or two next states, `x` and
`y`, depending on how you write your code.

Here's the original paper ["Regular Expression Search
Algorithm"](http://www.fing.edu.uy/inco/cursos/intropln/material/p419-thompson.pdf).
