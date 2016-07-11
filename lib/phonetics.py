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
English phonetics
'''

import functools

consonants = frozenset('DNSTZbdfghjklmnprstvwz')
vowels = frozenset('03@AEIOUVaeiou')

espeak = None

def init():
    '''
    initialize underlying speech engine
    '''
    global espeak
    from lib import espeak  # pylint: disable=redefined-outer-name
    espeak.init()
    espeak.set_voice_by_name('en')

@functools.lru_cache(maxsize=9999)
def text_to_phonemes(s):
    '''
    translate text to phonemes
    '''
    return espeak.text_to_phonemes(s)

__all__ = [
    'consonants',
    'vowels',
    'text_to_phonemes',
]

# vim:ts=4 sts=4 sw=4 et
