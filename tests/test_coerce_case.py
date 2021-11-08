# Copyright © 2016-2021 Jakub Wilk <jwilk@jwilk.net>
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

from tests.tools import (
    assert_equal,
    testcase,
)

import lib.misc as M

def t(src, word, exp):
    res = M.coerce_case(src, word)
    assert_equal(exp, res)

@testcase
def test_a():
    t('a', 'a', 'a')
    t('A', 'a', 'A')
    t('an', 'a', 'a')
    t('An', 'a', 'A')
    t('AN', 'a', 'A')

@testcase
def test_an():
    t('a', 'an', 'an')
    t('A', 'an', 'An')
    t('an', 'an', 'an')
    t('An', 'an', 'An')
    t('AN', 'an', 'AN')

del testcase

# vim:ts=4 sts=4 sw=4 et
