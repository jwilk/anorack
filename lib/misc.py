# Copyright © 2016-2022 Jakub Wilk <jwilk@jwilk.net>
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

import os
import sys

def warn(msg):
    '''
    print warning message
    '''
    prog = os.path.basename(sys.argv[0])
    print(f'{prog}: warning: {msg}', file=sys.stderr)

def _coerce_case(src, word):
    '''
    coerce word to the same case as src
    (simple version doesn't support title-case)
    '''
    if src.isupper():
        return word.upper()
    else:
        return word.lower()

def coerce_case(src, word):
    '''
    coerce word to the same case as src
    '''
    return (
        _coerce_case(src[:1], word[:1]) +
        _coerce_case(src[1:], word[1:])
    )

__all__ = [
    'warn',
    'coerce_case',
]

# vim:ts=4 sts=4 sw=4 et
