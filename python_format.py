from __future__ import print_function, division

from collections import namedtuple
from heapq import heappush, heappop
from itertools import tee, izip

import sys
sys.path.append('pypy')

from pypy.interpreter.pyparser.pytokenizer import generate_tokens
from pypy.interpreter.pyparser import pytoken
from pypy.interpreter.pyparser.pygram import tokens

def pairwise(it):
    a, b = tee(it)
    next(b, None)
    return izip(a, b)

Line = namedtuple('Line', ['indent_level', 'tokens'])
Spacer = namedtuple('Spacer', ['penalty', 'bracket_level'])

OPERATORS = [tokens.PLUS, tokens.MINUS, tokens.STAR, tokens.SLASH, tokens.VBAR,
             tokens.AMPER, tokens.LESS, tokens.GREATER, tokens.EQUAL,
             tokens.PERCENT, tokens.EQEQUAL, tokens.NOTEQUAL, tokens.LESSEQUAL,
             tokens.GREATEREQUAL, tokens.CIRCUMFLEX, tokens.LEFTSHIFT,
             tokens.RIGHTSHIFT, tokens.DOUBLESTAR, tokens.PLUSEQUAL,
             tokens.MINEQUAL, tokens.STAREQUAL, tokens.SLASHEQUAL,
             tokens.PERCENTEQUAL, tokens.AMPEREQUAL, tokens.VBAREQUAL,
             tokens.CIRCUMFLEXEQUAL, tokens.LEFTSHIFTEQUAL,
             tokens.RIGHTSHIFTEQUAL, tokens.DOUBLESTAREQUAL,
             tokens.DOUBLESLASH, tokens.DOUBLESLASHEQUAL]

KEYWORDS = ['class', 'if', 'def', 'return', 'for', 'while', 'elif', 'else', 'yield', 'in', 'pass', 'del']

COLUMN_WIDTH = 80
BRACE_PENALTY = 50
EXTRA_CHAR_PENALTY = 100

def newline_penalty(first, second):
    if first[0] in OPERATORS:
        return 10
    
    if second[0] in OPERATORS:
        return 100

    if first[0] == tokens.NAME and first[1] in KEYWORDS:
        return 20

    if first[0] == tokens.COMMA:
        return 1

    if first[0] == tokens.COLON:
        return 50

    if second[0] == tokens.COLON:
        return 10
    
    return float('inf')

def needs_space_between(first, second):
    if first[0] == tokens.NAME and first[1] in KEYWORDS:
        return True

    if second[0] == tokens.NAME and second[0] in KEYWORDS:
        return True

    if first[0] == tokens.COLON or second[0] == tokens.COLON:
        return True

    if first[0] in OPERATORS or second[0] in OPERATORS:
        return True

    if first[0] == tokens.NAME:
        return not second[0] in (tokens.LPAR, tokens.RPAR, tokens.LSQB, tokens.RSQB, tokens.DOT, tokens.COMMA)

    if second[0] == tokens.NAME:
        return not first[0] in (tokens.DOT, tokens.LPAR, tokens.LSQB)

    if first[0] == tokens.COMMA:
        return True
    
    return False

def get_variants(node, toks, brace_level, indent_level):
    first = toks[node[1]]
    second = toks[node[1] + 1]
    line_length = calc_line_length(node, toks, indent_level)
    base_penalty = newline_penalty(first, second) + (len(toks) - node[1]) / len(toks)
    needs_space = needs_space_between(first, second)

    if second[0] == tokens.COLON and second == toks[-1]:
        needs_space = False

    spacer = ' ' if needs_space else ''

    no_newline_len = line_length + len(spacer) + len(second[1])

    if no_newline_len > COLUMN_WIDTH:
        no_newline_penalty = (no_newline_len - COLUMN_WIDTH) * EXTRA_CHAR_PENALTY
    else:
        no_newline_penalty = 0

    variants = [(no_newline_penalty, spacer)]

    if base_penalty == float('inf'):
        return variants

    spacer = ''

    if brace_level == 0:
        spacer += ' \\\n'
    else:
        spacer += '\n'

    spacer += '    ' * (indent_level + 1)

    variants.append((base_penalty + brace_level * BRACE_PENALTY, spacer))
    return variants

def calc_line_length(node, tokens, indent_level):
    length = 0

    while not node is None:
        token = tokens[node[1]]
        length += len(token[1])
        newline_index = node[3].rfind('\n')

        if newline_index != -1:
            return length + (len(node[3]) - newline_index - 1)
        else:
            length += len(node[3])

        node = node[2]

    length += indent_level * 4
    return length

def calc_brace_level(node, toks):
    brace_level = 0

    while not node is None:
        token = toks[node[1]]
        
        if token[0] in (tokens.LPAR, tokens.LSQB, tokens.LBRACE):
            brace_level += 1
        elif token[0] in (tokens.RPAR, tokens.RSQB, tokens.RBRACE):
            brace_level -= 1

        node = node[2]

    return brace_level

def format_line(line):
    """
    line: Line object
    returns: Formatted line as a string
    """
    tokens = line.tokens

    if len(tokens) == 0:
        return ''

    # (penalty, token_idx, prev, prev_space)
    # newline: 0 - No newline, 1 - newline
    unvisited = [(0, 0, None, '')]

    while len(unvisited) > 0:
        node = heappop(unvisited)
        penalty, token_idx, prev, prev_space = node

        if token_idx >= len(tokens) - 1:
            break;
        
        token = tokens[token_idx]
        next_token = tokens[token_idx + 1]
        brace_level = calc_brace_level(node, tokens)
        variants = get_variants(node, tokens, brace_level, line.indent_level)
        #print(token[1])

        # variant: (penalty, str)
        for variant in variants:
            heappush(unvisited, (variant[0], token_idx + 1, node, variant[1]))

    nodes = []
    while not node is None:
        nodes.append(node)
        node = node[2]

    nodes.reverse()
    #print([n[0] for n in nodes])

    strs = ['    ' * line.indent_level]

    for _, token_idx, _, prev_space in nodes:
        strs.append(prev_space)
        token = tokens[token_idx]
        strs.append(token[1])

    return ''.join(strs)

def main(argv):
    toks = generate_tokens(sys.stdin.readlines(), 0)

    #for token in toks:
        #for key, value in pytoken.python_tokens.items():
            #if value == token[0]:
                #sys.stdout.write('{} ({}) '.format(key, token[1]))
                #if token[0] == tokens.NEWLINE:
                    #sys.stdout.write('\n')

    #sys.stdout.write('\n\n')

    indent_level = 0
    lines = []
    current_line = None
    
    for token in toks:
        if token[0] == tokens.INDENT:
            indent_level += 1
            continue
        elif token[0] == tokens.DEDENT:
            indent_level -= 1
            continue

        if current_line is None:
            current_line = Line(indent_level, [])
            lines.append(current_line)

        if token[0] == tokens.NEWLINE:
            current_line = None
        else:
            current_line.tokens.append(token)

    for line in lines:
        print(format_line(line))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

