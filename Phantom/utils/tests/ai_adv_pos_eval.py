#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Rigorously test the advanced position evaluator."""

from Phantom.core.game_class import ChessGame
from Phantom.ai.pos_eval.advanced import pos_eval_advanced
from Phantom.utils.debug import log_msg, clear_log
from Phantom.boardio.epd_read import load_test, list_tests

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.ai.pos_eval.advanced.pos_eval_advanced()', 0)
    for test in list_tests():
        log_msg('Beginning pos eval on test {}'.format(test), 0)
        board = load_test(test)
        score = None
        try:
            score = pos_eval_advanced(board)
        except Exception as e:
            log_msg('Advanced position evaluation failed: \n{}'.format(e), 0, err=True)
        finally:
            log_msg('Pos eval test on {} complete: score={}'.format(test, score), 0)
    log_msg('Test complete', 0)


if __name__ == '__main__':
    main()
