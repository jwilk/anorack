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

import lib.articles as M

@testcase
def test_choose_a():
    art = M.choose_art("sp'am")
    assert_equal(art, 'a')

@testcase
def test_choose_a_ipa():
    art = M.choose_art("θˈɜːmɪdˌɔː")
    assert_equal(art, 'a')

@testcase
def test_choose_an():
    art = M.choose_art("'Eg")
    assert_equal(art, 'an')

@testcase
def test_choose_an_ipa():
    art = M.choose_art("ˈɛɡ")
    assert_equal(art, 'an')

@testcase
def test_choose_other():
    art = M.choose_art('%')
    assert_equal(art, NotImplemented)
    art = M.choose_art('')
    assert_equal(art, NotImplemented)

del testcase

# vim:ts=4 sts=4 sw=4 et
