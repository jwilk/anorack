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

import functools

from nose.tools import (
    assert_equal,
)

from tests.tools import isolation

import lib.phonetics as M

def __test(word, xphon, xipa):
    M.init()
    phon = M.text_to_phonemes(word)
    assert_equal(xphon, phon)
    ipa = M.text_to_phonemes(word, ipa=True)
    assert_equal(xipa, ipa)
_test = isolation(__test)

def test_overrides():
    def t(word, xphon, xipa):
        return (
            functools.partial(_test, xphon=xphon, xipa=xipa),
            word
        )
    yield t('EWMH', ",i:d,Vb@Lj,u:,Em'eItS", 'ˌiːdˌʌbəljˌuːˌɛmˈeɪtʃ')
    yield t('UCS', "j,u:s,i:;'Es", 'jˌuːsˌiːˈɛs')
    yield t('UDP', "j,u:d,i:p'i:", 'jˌuːdˌiːpˈiː')
    yield t('UTF', "j,u:t,i:;'Ef", 'jˌuːtˌiːˈɛf')
    yield t('UTS', "j,u:t,i:;'Es", 'jˌuːtˌiːˈɛs')
    yield t('UUID', "j,u:j,u:,aId'i:", 'jˌuːjˌuːˌaɪdˈiː')
    yield t('unary', "j'un@ri", "jˈunəɹi")
    yield t('usr', "j,u:,Es'A@", "jˌuːˌɛsˈɑː")

# vim:ts=4 sts=4 sw=4 et
