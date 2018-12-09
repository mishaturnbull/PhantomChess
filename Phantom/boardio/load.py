# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Get a FEN string for a given board save-name."""

#from Phantom.core.exceptions import ChessError, LogicError
from Phantom.constants import save_fen, phantom_dir
import os
#import inspect

def valid_lines_from_file(file_path):
    with open(file_path) as in_file:
        return [line.strip() for line in in_file.readlines()
                if line.strip() and line.strip()[0] != '#']

def load_game(name):
    file_path = os.path.join(phantom_dir, 'boardio', save_fen)
    for line in valid_lines_from_file(file_path):
        bname, _, fen = line.partition(':')
        if bname.strip() == name:
            return fen.strip()

def list_games():
    file_path = os.path.join(phantom_dir, 'boardio', save_fen)
    return [line.partition(':')[0].strip() for line in valid_lines_from_file(file_path)]
