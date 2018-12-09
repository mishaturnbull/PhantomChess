# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""The basics of the basics."""

from Phantom.ai.settings import scores, colors, king_material

def pos_eval_basic(board):
    return sum(scores[p.ptype] * colors[p.color]
                  for p in board.pieces)

def pos_material(board):
    return sum(king_material if p.ptype == 'king' else scores[p.ptype]
                  for p in board.pieces)
