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
English parser
'''

import re

class Location(object):
    '''
    location in a file
    '''
    def __init__(self, file, lineno):
        self.file = file
        self.lineno = lineno

    def __str__(self):
        return '{path}:{n}'.format(path=self.file.name, n=self.lineno)

find_articles = re.compile(
    r'''\b(an?)\s+(?:['‘"“]\s*)?([^\W_]+)\b|\b(an?)\s*$''',
    re.IGNORECASE
).finditer

def parse_file(file):
    '''
    parse the file:
    return sequence of (<location>, <article>, <word>) tuples
    '''
    carry = ''
    for i, line in enumerate(file, start=1):
        cline = carry + line
        carry = ''
        for match in find_articles(cline):
            art, word, eol_art = match.groups()
            if art is not None:
                assert word is not None
                yield (Location(file, i), art, word)
            else:
                assert eol_art is not None
                carry = eol_art + ' '

__all__ = ['parse_file']

# vim:ts=4 sts=4 sw=4 et
