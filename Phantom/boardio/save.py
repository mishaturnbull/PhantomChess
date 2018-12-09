# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Save a game."""

from Phantom.constants import save_fen, phantom_dir
import os

# implementation detail 4

# format = '{name}: {fen}\n'

def save(board):
    write = os.path.join(phantom_dir, 'boardio', save_fen)
    newline = '{}: {}\n'.format(board.name, board.fen_str())
    with open(write, 'a') as f:
        f.write(newline)
