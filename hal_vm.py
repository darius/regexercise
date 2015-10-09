"""
A virtual machine meant to share enough of the IBM 7094's character to
run Thompson's code in an obvious direct translation, but to be easier
to quickly explain and visually animate. So the 'machine words' are
fixed-length strings with fields holding instruction mnemonics and
decimal numbers.
"""

import assembler
import re

## v = load('catfind.s', '')
## v.show()
#.               0   r2                r4                r6                r8             
#. r1                r3                r5                r7                r9             
#. 
#.  0 start          ==>set   4 0 20   20                40                60 ifne  1 C 13   80             
#.  3 advance         1 set   6 0 40   21                41                61 jump  9 0 11   81             
#. 11 next            2 set   7 0 40   22                42                62 ifne  1 A 13   82             
#. 13 fail            3 set   2 0  3   23                43                63 jump  9 0 11   83             
#. 20 states1         4 store 2 7  0   24                44                64 ifne  1 T 13   84             
#. 40 states2         5 set   7 4  0   25                45                65 found 0 0  0   85             
#. 60 code            6 set   4 6  0   26                46                66                86             
#.                    7 set   6 7  0   27                47                67                87             
#.                    8 getch 1 0  0   28                48                68                88             
#.                    9 set   8 4  0   29                49                69                89             
#.                   10 jump  0 0 60   30                50                70                90             
#.                   11 store 9 7  0   31                51                71                91             
#.                   12 set   7 7  1   32                52                72                92             
#.                   13 fetch 2 8  0   33                53                73                93             
#.                   14 set   8 8  1   34                54                74                94             
#.                   15 jump  0 2  0   35                55                75                95             
#.                   16                36                56                76                96             
#.                   17                37                57                77                97             
#.                   18                38                58                78                98             
#.                   19                39                59                79                99             
#. 

def toplevel(filename, inputs=''):
    vm = load(filename, inputs)
    vm.show()

def load(filename, inputs):
    return load_program(open(filename), inputs)

def load_program(program_lines, inputs):
    env = dict(('r%d'%i, i) for i in range(1, 10))
    words = assembler.assemble(assemble1, program_lines, env)
    return VM(words, inputs, env)

def assemble1(tokens, env):
    "Assemble a single line of source code."
    mnemonic, rest = tokens[0].lower(), ' '.join(tokens[1:])
    fields = [field.strip() or '0' for field in rest.split(',')]
    args = [eval(operand, {}, env) for operand in fields]
    if mnemonic == 'zeroes':
        assert len(args) == 1
        return [' '*9] * args[0]
    else:
        while len(args) < 3:
            args.append('0')
        assert len(args) == 3
        return ['%-5s%s%s%02s' % (mnemonic, args[0], args[1], int(args[2]))]

def show_env(env):
    return ['%2d %-12s' % (value, label)
            for label, value in sorted(env.items(), key=lambda kv: kv[1])
            if not re.match(r'r[1-9]|__here__', label)]

def put_number(vh, vn):
    assert len(vh) == 7
    assert isinstance(vn, int)
    vl = '%2d' % vn
    assert len(vl) == 2, vn
    return vh + vl

def get_number(v):
    assert len(v) == 9
    vh, vl = v[:7], v[7:]
    assert len(vl) == 2, repr(v)
    return vh, int('0' if vl == '  ' else vl)

def add(u, v):
    uh, un = get_number(u)
    vh, vn = get_number(v)
    rn = (un + vn + 100) % 100
    if not uh.strip(): return put_number(vh, rn)
    if not vh.strip(): return put_number(uh, rn)
    assert False
## add(' '*7+' 1', ' '*7+'-1')
#. '        0'

class VM(object):

    def __init__(self, program, input_chars, env):
        self.pc = put_number(' '*7, 0)
        self.M = [' '*9] * 100
        self.R = [' '*8+'0'] + [' '*9] * 9
        self.input_chars = iter(input_chars)
        self.env = env
        for addr, value in enumerate(program):
            assert len(value) == 9
            self.store(put_number(' '*7, addr), value)

    def show(self):
        regs = map(self.show_reg, range(10))
        print('\n'.join(format_columns(regs, 5)))
        print('')
        defs = pad(show_env(self.env), 20)
        insns = map(self.show_cell, range(100))
        print('\n'.join(format_columns(defs + list(insns), 6)))

    def show_reg(self, i):
        r = '  ' if i == 0 else 'r%d' % i
        word = self.R[i]
        return '%s %s %s %s %s' % (r, word[:5], word[5], word[6], word[7:])

    def show_cell(self, i):
        word = self.M[i]
        addr = '==>' if i == get_number(self.pc)[1] else '%2d ' % i
        return '%s%s %s %s %s' % (addr, word[:5], word[5], word[6], word[7:])

    def fetch(self, addr):
        ah, an = get_number(addr)
        return self.M[an]

    def store(self, addr, value):
        ah, an = get_number(addr)
        self.M[an] = value

    def get(self, r):
        return self.R[int(r)]

    def set(self, r, value):
        if int(r) != 0:
            self.R[int(r)] = value

    def run(self):
        while True:
            try:
                self.step()
            except Halt as e:
                return e.args[0]

    def step(self):
        insn = self.fetch(self.pc)
        self.pc = add(self.pc, put_number(' '*7, 1))
        op, r1, r2, addr = insn[:5], insn[5], insn[6], insn[7:]

        def ea():
            return add(self.get(r2), ' '*7 + addr)

        if   op == 'fetch':
            self.set(r1, self.fetch(ea()))
        elif op == 'store':
            self.store(ea(), self.get(r1))
        elif op == 'set  ':
            self.set(r1, ea())
        elif op == 'add  ':
            self.set(r1, add(self.get(r1), ea()))
        elif op == 'jump ':
            self.set(r1, self.pc)
            self.pc = ea()
        elif op == 'ifeq ':
            value = ' '*8 + r2
            if self.get(r1) == value:
                self.pc = ' '*7 + addr
        elif op == 'ifne ':
            value = ' '*8 + r2
            if self.get(r1) != value:
                self.pc = ' '*7 + addr
        elif op == 'getch':
            ch = next(self.input_chars, None)
            if ch is None:
                raise Halt(0, 'Out of input')
            self.set(r1, ' '*8 + ch)
        elif op == 'noop ' or op == '     ':
            pass
        elif op == 'halt ':
            value = ea()
            raise Halt(value, 'Found' if value else 'Not found')
        else:
            assert False, "Unknown instruction: %r" % op

class Halt(Exception): pass

def format_columns(items, ncols, sep='   '):
    items = list(items)
    assert items 
    assert all(len(item) == len(items[0]) for item in items)
    nrows = (len(items) + ncols-1) // ncols
    items = pad(items, nrows * ncols)
    columns = [items[i:i+nrows] for i in range(0, len(items), nrows)]
    return map(sep.join, zip(*columns))

def pad(items, n):
    return items + [' ' * len(items[0])] * (n - len(items))

## for row in format_columns(map(str, range(10)), 3): print row
#. 0   4   8
#. 1   5   9
#. 2   6    
#. 3   7    
#. 


if __name__ == '__main__':
    import sys
    toplevel(sys.argv[1])
