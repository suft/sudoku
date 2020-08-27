#!/usr/bin/env python3

import sys
import time
from blessed import Terminal

def main():
    PREV, DEBUG = (False, False)
    argc = len(sys.argv) - 1
    print(f'The script has {argc} arguments')
    print(f'Program name: {sys.argv[0]}')
    if argc != 1:
        print('Invalid arguments')
        sys.exit(1)
    term = Terminal()
    board = [' ' if c == '.' else c for c in sys.argv[1]]
    full = ['0' if c == '.' else c for c in sys.argv[1]]
    with term.fullscreen(), term.cbreak():
        display(term, '0001', tuple(board))
        while True:
            if DEBUG and not PREV:
                display(term, '0001', tuple(full))
            elif not DEBUG and PREV:
                display(term, '0001', tuple(board))
            line = readline(term)
            if line == 'exit':
                sys.exit(0)
            elif line == 'debug':
                PREV, DEBUG = (DEBUG, not DEBUG)
            else:
                pass

def display(term, name, board):
    p = lambda s, t: s.join([t * 3] * 3)
    pp = lambda s, t: s.join([t] * 3) 
    top = '╔' + pp('╦', p('╤', '═')) + '╗'
    numbers = ('║' + pp('│', ' %s ')) * 3 + '║'
    small = '╟' + pp('╫', p("┼","─")) + '╢'
    big = '╠' + pp('╬', p("╪","═")) + '╣'
    bottom = '╚' + pp('╩', p('╧', '═')) + '╝'
    divider = '%s'.join([' ' + ('─' * 11) + ' '] * 2)
    print(term.home + term.clear)
    print(term.center(divider % f'Puzzle {name}'))
    print(term.center(top))
    for i in range(9):
        print(term.center((numbers % board[i * 9: 9 + i * 9])))
        if i < 8:
            print(term.center(big if i % 3 == 2 else small))
    print(term.center(bottom))

def readline(term):
    line = ''
    prompt = '>>> '
    print(prompt, end='', flush=True)
    while True:
        k = term.inkey()
        if k.is_sequence:
            if k.code == term.KEY_BACKSPACE and line:
                line = line[:-1]
                backspace()
            if k.code == term.KEY_ENTER:
                backspace(line + prompt)
                return line
        elif k:
            line += k
            print(k, end='', flush=True)

def backspace(line = ' '):
    back = '\b \b' * len(line)
    print(back, end='', flush=True)

if __name__ == '__main__':
    main()
