# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""The code that makes the AI do stuff.  Although this AI doesn't do very smart stuff."""

from Phantom.core.board import Board
#from Phantom.core.coord.point import Coord
#from Phantom.core.exceptions import InvalidMove, InvalidDimension, ChessError, LogicError
import random

#def make_random_move(board):
#    with board.frozen():
#        piece = random.choice(board.pieces)
#    if len(piece.valid()) <= 0:
#        return make_random_move(board)
#    else:
#        move = random.choice(piece.valid())
#        board.game.move(piece.coord, move)
#    return True

def make_random_move(board):
    piece = random.choice(board.get_piece_list(color=board.turn))
    all_valid_moves = [x for x in piece.all_valid_moves]
    if all_valid_moves:
        dest = random.choice(all_valid_moves)
        return board.game.move(piece.fen_loc, dest)
    else:
        return make_random_move(board)

def main(clear=True):
    from Phantom.core.game_class import ChessGame
    board = ChessGame().board
    board.pprint()
    for i in xrange(105):
        print('make_random_move {}: {}'.format(i + 1, make_random_move(board)))
        board.pprint()
        winner = board.game.is_won()
        if winner:
            print('{} won this game in {} random moves.'.format(winner, (i + 1) / 2))
            break
    return(board.game.ai_rateing)

if __name__ == '__main__':
    print('=' * 80)
    score = main()
    print(score)
