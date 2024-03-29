# Copyright © 2016-2023 Jakub Wilk <jwilk@jwilk.net>
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
anorack CLI
'''

import argparse
import signal
import sys

from lib.articles import choose_art
from lib.io import (
    open_file,
)
from lib.misc import coerce_case, warn
from lib.parser import parse_file
from lib.phonetics import init as init_phonetics, text_to_phonemes
from lib.version import __version__

class ArgumentParser(argparse.ArgumentParser):
    '''
    ArgumentParser with exit status 1
    '''

    def exit(self, status=0, message=None):
        if status:
            status = 1
        argparse.ArgumentParser.exit(self, status=status, message=message)

class VersionAction(argparse.Action):
    '''
    argparse --version action
    '''

    def __init__(self, option_strings, dest=argparse.SUPPRESS):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            help='show version information and exit'
        )

    def __call__(self, parser, namespace, values, option_string=None):
        from lib import espeak  # pylint: disable=import-outside-toplevel
        print(f'{parser.prog} {__version__}')
        print('+ Python {0}.{1}.{2}'.format(*sys.version_info))
        ng = ' NG' if espeak.ng else ''
        print(f'+ eSpeak{ng} {espeak.version}')
        parser.exit()

def check_word(loc, art, word, *, ipa=False):
    '''
    check if the word has correct article
    '''
    phon = text_to_phonemes(word, ipa=ipa)
    correct_art = choose_art(phon)
    if correct_art is NotImplemented:
        warn(f"can't determine correct article for {word!r} /{phon}/")
    elif art.lower() != correct_art:
        correct_art = coerce_case(art, correct_art)
        print(f'{loc}: {art} {word} -> {correct_art} {word} /{phon}/')
        return False
    return True

def main():
    '''
    run the program
    '''
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = ArgumentParser(description='"a" vs "an" checker')
    ap.add_argument('--version', action=VersionAction)
    ap.add_argument('-e', action='store_true', help='exit with non-zero status if issues were found')
    ap.add_argument('--ipa', action='store_true', help='use IPA instead of ASCII phoneme mnemonics')
    ap.add_argument('--traceback', action='store_true', help=argparse.SUPPRESS)
    ap.add_argument('files', metavar='FILE', nargs='*', default=['-'],
        help='file to check (default: stdin)')
    options = ap.parse_args()
    init_phonetics()
    ok = True
    rc = 0
    for path in options.files:
        try:
            file = open_file(path, encoding=sys.stdout.encoding, errors='replace')
        except OSError as exc:
            if options.traceback:
                raise
            msg = f'{ap.prog}: {path}: {exc.strerror}'
            print(msg, file=sys.stderr)
            rc = 1
            continue
        with file:
            for loc, art, word in parse_file(file):
                ok &= check_word(loc, art, word, ipa=options.ipa)
    if rc == 0 and options.e and not ok:
        rc = 2
    sys.exit(rc)

__all__ = ['main']

# vim:ts=4 sts=4 sw=4 et
