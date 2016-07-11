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
the command-line interface
'''

import argparse
import concurrent.futures
import functools
import io
import multiprocessing
import sys

from lib.articles import choose_art
from lib.io import (
    get_encoding,
    open_file,
)
from lib.misc import warn
from lib.parser import parse_file
from lib.phonetics import init as init_phonetics, text_to_phonemes
from lib.version import __version__

class VersionAction(argparse.Action):
    '''
    argparse --version action
    '''

    def __init__(self, option_strings, dest=argparse.SUPPRESS):
        super(VersionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            help="show program's version information and exit"
        )

    def __call__(self, parser, namespace, values, option_string=None):
        from lib import espeak
        print('{prog} {0}'.format(__version__, prog=parser.prog))
        print('+ Python {0}.{1}.{2}'.format(*sys.version_info))
        print('+ eSpeak {0}'.format(espeak.version))
        parser.exit()

def check_word(loc, art, word):
    '''
    check if the word has correct article
    '''
    phon = text_to_phonemes(word)
    correct_art = choose_art(phon)
    if correct_art is NotImplemented:
        warn("can't determine correct article for {word!r} /{phon}/".format(word=word, phon=phon))
    elif art.lower() != correct_art:
        print('{loc}: {art} {word} -> {cart} {word} /{phon}/'.format(
            loc=loc,
            art=art,
            cart=correct_art,
            word=word,
            phon=phon,
        ))

def parse_jobs(s):
    '''
    --jobs=N parser
    '''
    if s == 'auto':
        try:
            return multiprocessing.cpu_count()
        except NotImplementedError:
            return 1
    n = int(s)
    if n <= 0:
        raise ValueError
    return n
parse_jobs.__name__ = 'jobs'

def main():
    '''
    run the program
    '''
    ap = argparse.ArgumentParser(description='"a" vs "an" checker')
    ap.add_argument('--version', action=VersionAction)
    ap.add_argument('-j', '--jobs', type=parse_jobs, metavar='N', default=1, help='use N processes')
    ap.add_argument('files', metavar='FILE', nargs='*', default=['-'],
        help='file to check (default: stdin)')
    options = ap.parse_args()
    encoding = get_encoding()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding)
    init_phonetics()
    if len(options.files) <= 1 or options.jobs <= 1:
        for path in options.files:
            check_file(path, encoding=encoding)
    else:
        map_options = {}
        if sys.version_info >= (3, 5):
            chunksize = max(1, int(len(options.files) ** 0.5))  # wild guess
            map_options.update(chunksize=chunksize)
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=options.jobs)
        with executor:
            check_file_opt = functools.partial(check_file_s, encoding=encoding)
            for s in executor.map(check_file_opt, options.files, **map_options):
                sys.stdout.write(s)

def check_file(path, *, encoding):
    '''
    check one file
    '''
    file = open_file(path, encoding=encoding, errors='replace')
    with file:
        for loc, art, word in parse_file(file):
            check_word(loc, art, word)

def check_file_s(path, *, encoding):
    '''
    check_file() with captured stdout
    '''
    orig_stdout = sys.stdout
    sys.stdout = io_stdout = io.StringIO()
    try:
        check_file(path, encoding=encoding)
    finally:
        sys.stdout = orig_stdout
    return io_stdout.getvalue()

__all__ = ['main']

# vim:ts=4 sts=4 sw=4 et
