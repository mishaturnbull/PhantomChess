#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Test the boardio's load functions."""

from Phantom.boardio.load import load_game, list_games
from Phantom.core.board import load
from Phantom.boardio.epd_read import load_epd, load_test, list_tests
from Phantom.utils.debug import log_msg, clear_log

def main(clear=True):
    if clear: clear_log()
    log_msg('Beginning Phantom.core.boardio load functions test', 0)
    try:
        log_msg('Testing FEN load...', 0)
        name = list_games()[0]
        game = load(name)
    except Exception as e:
        log_msg('Test failed: {}'.format(e), 0, err=True)
    finally:
        log_msg('FEN load test complete.', 0)

    try:
        log_msg('Testing EPD load...', 0)
        name = list_tests()[0]
        game = load_test(name)
    except Exception as e:
        log_msg('Test failed: {}'.format(e), 0, err=True)
    finally:
        log_msg('EPD load test complete.', 0)

    log_msg('Phantom.core.boardio load functions test complete.', 0)

if __name__ == '__main__':
    main()
