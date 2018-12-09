#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Test the Phantom.core.board.Board.move() method"""

#from Phantom.core.board import Board
from Phantom.core.game_class import ChessGame
from Phantom.utils.debug import log_msg, clear_log

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.core.board.Board.move() method', 0)
    #b = Board(None)  # white to move, opening layout
    b = ChessGame().board
    try:
        b.move('e2e4')
        b.move('g8f6')
        b.move('g2g3')
    except Exception as e:
        log_msg('Phantom.core.board.Board.move() method test failed:\n{}'.format(e), 0, err=True)
    finally:
        log_msg('Test complete', 0)

if __name__ == '__main__':
    main()
