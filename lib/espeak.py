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
interface to eSpeak (NG)
'''

import ctypes
import distutils.version

try:
    _shlib = ctypes.CDLL('libespeak-ng.so.1')
    ng = True
except OSError:  # no coverage
    _shlib = ctypes.CDLL('libespeak.so.1')
    ng = False

# const char *espeak_Info(const char **path_data)
_info = _shlib.espeak_Info
_info.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
_info.restype = ctypes.c_char_p

def info():
    '''
    return eSpeak version information
    '''
    dummy = ctypes.c_char_p(b'')
    res = _info(ctypes.byref(dummy))
    return res.decode('ASCII')
version = distutils.version.LooseVersion(info().split()[0])
del info

# int espeak_Initialize(espeak_AUDIO_OUTPUT output, int buflength, const char *path, int options)
_initialize = _shlib.espeak_Initialize
_initialize.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
_initialize.restype = ctypes.c_int

def init():
    '''
    initialize eSpeak
    '''
    rc = _initialize(0, 0, None, 0)
    if rc <= 0:
        raise RuntimeError('espeak_Initialize(): internal error')  # no coverage

# espeak_ERROR espeak_SetVoiceByName(const char *name)
_set_voice_by_name = _shlib.espeak_SetVoiceByName
_set_voice_by_name.argtypes = [ctypes.c_char_p]
_set_voice_by_name.restype = ctypes.c_int

def set_voice_by_name(s):
    '''
    use this voice for synthesis
    '''
    s = s.encode('ASCII')
    rc = _set_voice_by_name(s)
    if rc == 0:
        return
    else:  # no coverage
        if rc == -1:
            msg = 'internal error'
        elif rc == 1:
            msg = 'the command could not be buffered'
        else:
            msg = 'unknown error {}'.format(rc)
        raise RuntimeError('espeak_SetVoiceByName(): ' + msg)

if version >= '1.48.1':

    # const char *espeak_TextToPhonemes(const void **textptr, int textmode, int phonememode)
    _text_to_phonemes = _shlib.espeak_TextToPhonemes
    _text_to_phonemes.restype = ctypes.c_char_p
    _text_to_phonemes.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int]

    def text_to_phonemes(s, *, ipa=False):
        '''
        translate text to phonemes
        '''
        s = s.encode('UTF-8')
        z = ctypes.c_char_p(s)
        zptr = ctypes.pointer(z)
        assert zptr.contents is not None
        if version >= '1.48.11':
            ipa = ipa << 1
        else:
            ipa = ipa << 4  # no coverage
        res = _text_to_phonemes(zptr, 1, ipa)
        if zptr.contents.value is not None:
            raise RuntimeError  # no coverage
        return res.decode('UTF-8').strip()

elif version >= '1.47.08':  # no coverage

    # void espeak_TextToPhonemes(const void *text, char *buffer, int size, int textmode, int phonememode)
    _text_to_phonemes = _shlib.espeak_TextToPhonemes
    _text_to_phonemes.restype = ctypes.c_char_p
    _text_to_phonemes.argtypes = [
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_char), ctypes.c_int,
        ctypes.c_int, ctypes.c_int
    ]

    def text_to_phonemes(s, *, ipa=False):
        '''
        translate text to phonemes
        '''
        s = s.encode('UTF-8')
        bufsize = 250
        buf = ctypes.create_string_buffer(bufsize)
        _text_to_phonemes(s, buf, bufsize, 1, ipa << 4)
        return buf.value.decode('UTF-8').strip()

else:  # no coverage

    raise RuntimeError('eSpeak >= 1.47.08 is required')

__all__ = [
    'init',
    'ng',
    'set_voice_by_name',
    'text_to_phonemes',
    'version',
]

# vim:ts=4 sts=4 sw=4 et
