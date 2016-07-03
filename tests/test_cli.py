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

import contextlib
import io
import sys

from nose.tools import (
    assert_equal,
)

import lib.cli as M

@contextlib.contextmanager
def mock_sys(argv, stdin, stdout, stderr):
    (orig_argv, orig_stdin, orig_stdout, orig_stderr) = (sys.argv, sys.stdin, sys.stdout, sys.stderr)
    try:
        (sys.argv, sys.stdin, sys.stdout, sys.stderr) = (argv, stdin, stdout, stderr)
        yield
    finally:
        (sys.argv, sys.stdin, sys.stdout, sys.stderr) = (orig_argv, orig_stdin, orig_stdout, orig_stderr)

def TextIO(s=None, *, name):
    fp = io.BytesIO(s)
    fp.name = name
    return io.TextIOWrapper(fp, encoding='UTF-8')

def t(*, stdin=None, files=None, stdout, stderr=''):
    mock_argv = ['anorack']
    if files is not None:
        raise NotImplementedError
    if stdin is not None:
        if isinstance(stdin, list):
            stdin = ''.join(line + '\n' for line in stdin)
        if isinstance(stdin, str):
            stdin = stdin.encode('UTF-8')
        mock_stdin = TextIO(stdin, name=sys.__stdin__.name)
    else:
        mock_stdin = sys.stdin
    mock_stdout = TextIO(name=sys.__stdout__.name)
    mock_stderr = TextIO(name=sys.__stderr__.name)
    def run_main():
        M.main()
        sys.stdout.flush()
        for fp in (sys.stdout, sys.stderr):
            s = fp.buffer.getvalue()  # pylint: disable=no-member
            yield s.decode('UTF-8')
    with mock_sys(mock_argv, mock_stdin, mock_stdout, mock_stderr):
        (actual_stdout, actual_stderr) = run_main()
    if isinstance(stdout, list):
        stdout = ''.join(line + '\n' for line in stdout)
    assert_equal(stdout, actual_stdout)
    assert_equal(stderr, actual_stderr)

def test_stdin():
    t(
        stdin=[
            'It could be carried by an African swallow!',
            'Oh, yeah, a African swallow maybe, but not an',
            'European swallow.'
        ],
        stdout=[
            "<stdin>:2: a African -> an African /'afrIk@n/",
            "<stdin>:3: an European -> a European /j,U@r-@p'i@n/"
        ]
    )

# vim:ts=4 sts=4 sw=4 et
