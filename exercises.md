Some coding exercises, working up to matching regular expressions with Thompson's algorithm.

I'm assuming you know what a regular expression is and you're a fairly
experienced programmer. I don't know if these exercises are either fun or
effective -- please comment or fork here or email withal@gmail.com to help me
improve them.

## The problems

**First**, given a list of strings, and a stream of characters, read the
stream and report as soon as one of the strings occurs in it. (You
don't have to report which one.) For example, in Python we might ask

    >>> stream = iter('a cat is fat')
    >>> search(['rat', 'cat'], stream)  # Return position after first match, or None
    5
    >>> ''.join(stream)  # The rest wasn't consumed, see:
    ' is fat'

**Second:** As before, but instead of a list of strings, we take a
restricted kind of regular expression. You can represent these
expressions however you like; define three constructors:

* `literal(character)` should represent a regex matching just that character.
* `either(regex1, regex2)` should match what either regex1 or
regex2 matches; i.e. it represents `regex1|regex2`.
* `chain(regex1, regex2)` matches a match of `regex1` followed
by a match of `regex2`; i.e. it represents `regex1 regex2`.

So you could encode the same pattern as before as

    >>> def sequence(regexes): return reduce(chain, regexes)
    >>> rat_or_cat = either(sequence(map(literal, 'rat')), sequence(map(literal, 'cat')))

and then `search2(rat_or_cat, stream)` should produce the same
result. Of course one way to solve this is, just expand the pattern
into a list of strings and call `search1`. But this list could get
exponentially bigger than the regular expression -- consider

    >>> bit = either(literal('0'), literal('1'))
    >>> ten_bits = sequence(10 * [bit])

`ten_bits`, a regex with 20 literals, would expand out to a list of 1024
strings. (Also, we're soon going to add in a repetition operator
that'd make the set of matching strings infinite.) So now you want to
work with a more tailored representation.

**Third:** Now with one more regex constructor:

* `plus(regex)` has matches consisting of 1 or more matches of `regex` in sequence.
(The Kleene plus: `(regex)+` in the usual notation.)

**Fourth:** Replace the `plus` constructor with `star`, matching 0 or more.
Getting the matching to terminate can be tricky for patterns like `star(star(regex))` and you 
might prefer to just declare you won't handle such cases.

**Fifth:** Don't allocate any memory inside the main matching loop. (Some 
languages would make satisfying the letter of this requirement more painful than
it's worth; so it's enough if there's an obvious translation into an allocation-free
loop in a lower-level language.)

**Sixth:** Compile the regex, before the start of matching, into a machine-code program to
run at match time. I'll define a simple machine language for this, since the IBM 7094 that
Thompson used was kind of tricky and obscure. (To be written.)

**Bonus:** Add a `both(regex1, regex2)` constructor that matches when both of its
arguments match.

## General hints

For all these problems you can keep a set of states of some kind; in the main loop you
ask if any of the states is the matched state, and if not, get the next character from
the stream and update the state-set according to it. For the first problem [here's
pseudocode](http://stackoverflow.com/a/846728/27024) (in the first part of the answer;
it assumes there's just one pattern string, but generalizes easily).

What kind of states will work for the subsequent problems? Essentially, regular 
expressions again: if a state represents a regular expression r, and you get input
character c, then the [Brzozowski derivative](http://blog.sigfpe.com/2005/05/derivatives-of-regular-expressions.html)
dr/dc is the next state. Thompson represents dr/dc as a set of 0 or more possible
next states. If r is `ax|ay` and c is `a`, then you could get either one next state,
`x|y`, or two next states, `x` and `y`, depending on how you write your code.

Here's the original paper ["Regular Expression Search Algorithm"](http://www.fing.edu.uy/inco/cursos/intropln/material/p419-thompson.pdf).