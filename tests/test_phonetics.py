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

from nose.tools import (
    assert_equal,
)

from tests.tools import isolation

import lib.phonetics as M

def _test_overrides():
    def t(word, xphon):
        phon = M.text_to_phonemes(word)
        assert_equal(xphon, phon)
    M.init()
    t('EWMH', ",i:d,Vb@Lj,u:,Em'eItS")
    t('UCS', "j,u:s,i:;'Es")
    t('UDP', "j,u:d,i:p'i:")
    t('UTF', "j,u:t,i:;'Ef")
    t('UTS', "j,u:t,i:;'Es")
    t('UUID', "j,u:j,u:,aId'i:")
    t('unary', "j'un@ri")
    t('usr', "j,u:,Es'A@")
test_overrides = isolation(_test_overrides)
test_overrides.__name__ = 'test_overrides'

# vim:ts=4 sts=4 sw=4 et
