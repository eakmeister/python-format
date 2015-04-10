from __future__ import print_function, division

import sys

from pypy.interpreter.pyparser.pytokenizer import generate_tokens
from pypy.interpreter.pyparser import pytoken
from pypy.interpreter.pyparser.pygram import tokens

def main(argv):
    lines = sys.stdin.readlines()
    toks = generate_tokens(lines, 0)

    for token in toks:
        for key, value in pytoken.python_tokens.items():
            if value == token[0]:
                sys.stdout.write('{} ({}) '.format(key, token[1]))
                if token[0] == tokens.NEWLINE:
                    sys.stdout.write('\n')

    sys.stdout.write('\n\n')

    indent_level = 0
    first_tok = True
    
    for token in toks:
        if token[0] == tokens.INDENT:
            indent_level += 1
            continue
        elif token[0] == tokens.DEDENT:
            indent_level -= 1
            continue

        if first_tok:
            sys.stdout.write('    ' * indent_level)
            first_tok = False

        if token[0] == tokens.NEWLINE:
            sys.stdout.write('\n')
            first_tok = True
        else:
            sys.stdout.write(token[1])

if __name__ == '__main__':
    sys.exit(main(sys.argv))

