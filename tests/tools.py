# Copyright © 2016-2022 Jakub Wilk <jwilk@jwilk.net>
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

import concurrent.futures
import functools
import multiprocessing
import sys
import unittest

def isolation(f):
    if 'coverage' in sys.modules:
        # Process isolation would break coverage measurements.
        # Oh well. FIXME.
        return f
    else:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            mp_context = multiprocessing.get_context('fork')
            with concurrent.futures.ProcessPoolExecutor(max_workers=1, mp_context=mp_context) as executor:
                ftr = executor.submit(f, *args, **kwargs)
                return ftr.result()
    return wrapper

def testcase(f):
    class TestCase(unittest.TestCase):  # pylint: disable=redefined-outer-name
        @staticmethod
        def test():
            return f()
        def __str__(self):
            return f'{f.__module__}.{f.__name__}'
    return TestCase

tc = unittest.TestCase('__hash__')

assert_equal = tc.assertEqual
assert_is = tc.assertIs
assert_is_instance = tc.assertIsInstance
assert_not_equal = tc.assertNotEqual

del tc

class TestCase(unittest.TestCase):
    def __str__(self):
        cls = unittest.util.strclass(self.__class__)
        name = self._testMethodName
        return f'{cls}.{name}'

__all__ = [
    'isolation',
    'testcase',
    'TestCase',
    # nose-compatible:
    'assert_equal',
    'assert_is',
    'assert_is_instance',
    'assert_not_equal',
]

# vim:ts=4 sts=4 sw=4 et
