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

import io

from nose.tools import (
    assert_equal,
    assert_is,
    assert_is_instance,
)

import lib.parser as M

def t(s, exp):
    file = io.StringIO(s)
    result = list(M.parse_file(file))
    assert_equal(len(result), len(exp))
    for (loc, art, word), (xi, xart, xword) in zip(result, exp):
        assert_is_instance(loc, M.Location)
        assert_is(loc.file, file)
        assert_equal(loc.lineno, xi)
        assert_equal(xart, art)
        assert_equal(xword, word)

def test_mid_line():
    t('Oh, yeah, an African swallow maybe,\nbut not a European swallow.\n', [
        (1, 'an', 'African'),
        (2, 'a', 'European'),
    ])

def test_wrapped():
    t('I thought we were an\nautonomous collective.', [
        (2, 'an', 'autonomous'),
    ])

def test_quotes():
    t(
        "a 'scratch'\n"
        'a ‘scratch’\n'
        'a "scratch"\n'
        'a “scratch”\n',
        [(i, 'a', 'scratch') for i in range(1, 5)]
    )

# vim:ts=4 sts=4 sw=4 et
