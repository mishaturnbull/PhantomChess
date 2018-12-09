# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Phases of the game: opening, midgame, endgame.

"""

class Phase (object):
    opening, midgame, endgame = range(3)

    @staticmethod
    def analyze(board):
        from Phantom.ai.pos_eval.basic import pos_material
        from Phantom.ai.settings import (max_material, min_material, opening_range,
                                         midgame_range, endgame_range, opening_moves)
        m = pos_material(board)
        ret = Phase.opening

        if m in opening_range:
            ret = Phase.opening
        elif m in midgame_range:
            ret = Phase.midgame
        elif m in endgame_range:
            ret = Phase.endgame

        if board.fullmove_clock < opening_moves:
            ret = Phase.opening
        else:
            if ret == Phase.opening:
                ret = Phase.midgame

        # check queen movement status
        queens = []
        for piece in board.pieces:
            if piece.ptype == 'queen':
                queens.append(piece)
        if all([not q.first_move for q in queens]):
            if ret == Phase.opening:
                ret = Phase.midgame

        return ret

