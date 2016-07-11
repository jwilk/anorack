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
I/O and encodings
'''

import codecs
import io
import sys

def enc_eq(e1, e2):
    '''
    check if two encodings are equal
    '''
    return (
        codecs.lookup(e1).name ==
        codecs.lookup(e2).name
    )

def get_encoding():
    '''
    get locale encoding (from sys.stdout);
    upgrade ASCII to UTF-8
    '''
    locale_encoding = sys.stdout.encoding
    if enc_eq(locale_encoding, 'ASCII'):
        return 'UTF-8'
    else:
        return locale_encoding

def open_file(path, *, encoding, errors):
    '''
    open() with special case for "-"
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
    'get_encoding',
    'open_file',
]

# vim:ts=4 sts=4 sw=4 et
