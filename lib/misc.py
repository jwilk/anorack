# Copyright © 2016 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
miscellanea
'''

import io
import sys

consonants = frozenset('DSTZbdfghjklmnprstvwz')
vowels = frozenset('03@AEIOUVaeiou')

def choose_art(phon):
    try:
        p = phon.strip(",'")[0]
    except IndexError:
        return NotImplemented
    if p in consonants:
        return 'a'
    elif p in vowels:
        return 'an'
    else:
        return NotImplemented

def warn(msg):
    print('anorack: warning: ' + msg, file=sys.stderr)

def open_file(path, *, encoding, errors):
    '''
    open() with special case for “-”
    '''
    if path == '-':
        return io.TextIOWrapper(
            sys.stdin.buffer,
            encoding=encoding,
            errors=errors,
        )
    else:
        return open(
            path, 'rt',
            encoding=encoding,
            errors=errors,
        )

__all__ = [
    'choose_art',
    'open_file',
    'warn',
]

# vim:ts=4 sts=4 sw=4 et
