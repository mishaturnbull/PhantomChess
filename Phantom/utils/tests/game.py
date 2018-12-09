#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Test the game class itself."""

from Phantom.core.game_class import ChessGame
from Phantom.utils.debug import log_msg, clear_log

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.core.board.Board.__init__() method', 0)
    g = None
    try:
        g = ChessGame()
    except Exception as e:
        log_msg('ChessGame instantiation test failed:\n{}'.format(e), 0, err=True)
    finally:
        log_msg('Test complete', 0)
    return g

if __name__ == '__main__':
    main()
