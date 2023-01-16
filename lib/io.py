# Copyright © 2016-2023 Jakub Wilk <jwilk@jwilk.net>
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

def get_encoding(file):
    '''
    get file encoding (from sys.stdout);
    upgrade ASCII to UTF-8
    '''
    encoding = file.encoding
    if enc_eq(encoding, 'ASCII'):
        return 'UTF-8'
    else:
        return encoding

def wrap_file(file):
    '''
    wrap file to upgrade encoding from ASCII to UTF-8
    '''
    new_encoding = get_encoding(file)
    if new_encoding == file.encoding:
        return file
    return io.TextIOWrapper(
        file.buffer,
        encoding=new_encoding,
        line_buffering=file.line_buffering
    )

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
        return open(  # pylint: disable=consider-using-with
            path, 'rt',
            encoding=encoding,
            errors=errors,
        )

__all__ = [
    'get_encoding',
    'open_file',
]

# vim:ts=4 sts=4 sw=4 et
