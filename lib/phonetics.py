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

'''
English phonetics
'''

import functools
import os

consonants = frozenset(
    'DNSTZbdfghjklmnprstvwz'
    'ðŋʃθʒbdfɡhjkɬmnpɹstvwz'
)
vowels = frozenset(
    '03@AEIOUVaeiou'
    'ɒɜəɑɛɪɔʊʌɐeiɔu'
)
accents = frozenset(
    ",'"
    "ˌˈ"
)

espeak = None
overrides = {}

def init():
    '''
    initialize underlying speech engine
    '''
    global espeak  # pylint: disable=global-statement,global-variable-not-assigned
    from . import espeak  # pylint: disable=redefined-outer-name,import-outside-toplevel
    espeak.init()
    espeak.set_voice_by_name('en')
    libdir = os.path.dirname(__file__)
    if __package__ == 'lib':
        basedir = f'{libdir}/..'
    else:
        basedir = libdir
    # Ideally false positives should be fixed in eSpeak,
    # but as a stop-gap measure, we carry data file to correct some of them.
    path = f'{basedir}/data/overrides'
    with open(path, 'rt', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            (word, phon) = line.split('\t', 1)
            word = word.lower()
            overrides[word] = phon

@functools.lru_cache(maxsize=9999)
def text_to_phonemes(s, *, ipa=False):
    '''
    translate text to phonemes
    '''
    s = overrides.get(s.lower(), s)
    if s.startswith('[[') and s.endswith(']]'):
        return s.split('\t')[ipa][2:-2]
    else:
        return espeak.text_to_phonemes(s, ipa=ipa)

__all__ = [
    'consonants',
    'vowels',
    'accents',
    'text_to_phonemes',
]

# vim:ts=4 sts=4 sw=4 et
