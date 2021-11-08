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
    isolation,
    testcase,
    TestCase,
)

import lib.phonetics as M

def __test(word, xphon, xipa):
    M.init()
    phon = M.text_to_phonemes(word)
    assert_equal(xphon, phon)
    ipa = M.text_to_phonemes(word, ipa=True)
    ipa = ipa.replace('t͡ʃ', 'tʃ')
    assert_equal(xipa, ipa)
_test = isolation(__test)

class test_overrides(TestCase):
    pass

def _init_test_overrides():
    def add(word, xphon, xipa):
        @staticmethod
        def test():
            _test(word, xphon, xipa)
        setattr(test_overrides, 'test_' + word, test)
    add('EWMH', ",i:d,Vb@Lj,u:,Em'eItS", 'ˌiːdˌʌbəljˌuːˌɛmˈeɪtʃ')
    add('UCS', "j,u:s,i:;'Es", 'jˌuːsˌiːˈɛs')
    add('UDP', "j,u:d,i:p'i:", 'jˌuːdˌiːpˈiː')
    add('UPS', "j,u:p,i:;'Es", 'jˌuːpˌiːˈɛs')
    add('UTF', "j,u:t,i:;'Ef", 'jˌuːtˌiːˈɛf')
    add('UTS', "j,u:t,i:;'Es", 'jˌuːtˌiːˈɛs')
    add('UUID', "j,u:j,u:,aId'i:", 'jˌuːjˌuːˌaɪdˈiː')
    add('src', "s'o@s", 'sˈɔːs')
    add('unary', "j'un@ri", "jˈunəɹi")
    add('usr', "j,u:,Es'A@", "jˌuːˌɛsˈɑː")
_init_test_overrides()
del _init_test_overrides

del testcase

# vim:ts=4 sts=4 sw=4 et
