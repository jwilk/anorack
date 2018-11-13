'''
anorack's private modules
'''

import sys

type(...)  # Python >= 3 is required
if sys.version_info < (3, 2):  # no coverage
    raise RuntimeError('Python >= 3.2 is required')

__all__ = []

# vim:ts=4 sts=4 sw=4 et
