# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Determine if your platform supports printing of unicode characters."""

# See: http://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
# Windows users could try running 'chcp 65001' before running Phantom

import sys

def can_print_unicode(msg='Welcome to PhantomChess...'):
    try:
        print(str(u'♜ ♞ ♝ {} ♗ ♘ ♖ '.format(msg)))
        return True
    except UnicodeEncodeError:
        print(msg)
        return False

if __name__ == '__main__':
    print(can_print_unicode())
