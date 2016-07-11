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

try:
    import unittest.mock as mock
except ImportError:
    import mock  # pylint: disable=import-error

from nose.tools import (
    assert_equal,
)

import lib.io as M

def t(src, dst):
    class mock_stdout:
        encoding = src
    with mock.patch('sys.stdout', mock_stdout):
        encoding = M.get_encoding()
    assert_equal(encoding, dst)

def test_ascii():
    t('ANSI_X3.4-1968', 'UTF-8')
    t('US-ASCII', 'UTF-8')
    t('ASCII', 'UTF-8')

def test_8bit():
    t('ISO-8859-2', 'ISO-8859-2')

def test_utf8():
    t('UTF-8', 'UTF-8')

# vim:ts=4 sts=4 sw=4 et
