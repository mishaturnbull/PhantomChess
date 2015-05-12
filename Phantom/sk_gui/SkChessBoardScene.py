#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# This file is part of PhantomChess.                                    #
#                                                                       #
# PhantomChess is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# PhantomChess is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with PhantomChess.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os, sk, sound, ui
#from create_pieces_sprite_dict import GameScene
from Phantom.core.coord.point import Coord
from Phantom.core.pieces import ChessPiece
from Phantom.core.game_class import ChessGame
import Phantom.constants as C

img_dir = '../gui_pythonista/imgs'
img_dir = 'imgs'

#print(__name__)

class sk_BoardSquare(sk.SpriteNode):
    tile_size = sk.Size(C.scale_factor, C.scale_factor)

    def __init__(self, tile):
        sk.SpriteNode.__init__(self) # , sk.Texture(tile.color))
        self.alpha = 0.3
        self.color = tile.color
        self.name = tile.as_chess
        x, y = tile.as_screen
        self.position = (x-80, y+48)  # magic numbers!!
        self.size = self.tile_size

    def __contains__(self, touch_or_point):  # if touch in sk_BoardSquare
        try:
            return self.frame.contains_point(touch_or_point.location)
        except AttributeError:
            return self.frame.contains_point(touch_or_point)


class sk_ChessPiece(sk.SpriteNode):
    fmt = os.path.join(img_dir, 'Chess set images {}.jpg')
    piece_size = sk.Size(C.scale_factor-2, C.scale_factor-2)

    def __init__(self, piece):
        assert piece and isinstance(piece, ChessPiece)
        #piece_name = piece_name or 'white queen'
        #piece_name = piece_name.rpartition(' ')[0]  # white queen 0 --> white queen
        #print(os.d, self.fmt.format(piece_name))
        
        sk.SpriteNode.__init__(self, sk.Texture(self.fmt.format(piece.name)))
        self.alpha = 0.5
        self.piece = piece
        #self.name = piece_name
        #self.size = self.tile_size
        self.prev_position = self.position
        self.touch_enabled = True

    @property
    def name(self):
        return self.piece.name

    #def touch_began(self, node, touch):
    #    print('touch_began({}, {}, {})'.format(self, node, touch))
    #    self.prev_position = self.position

    # this is not a setter because we want touch_moved() and
    # touch_ended() to set position without setting prev_position
    def set_position(self, position):
        self.prev_position = self.position = position

    def undo_position(self):
        self.position = self.prev_position

    def is_move_valid(self, target):
        return self.piece.is_move_valid(Coord.from_chess(target))

    def move(self, target):
        return self.piece.move(Coord.from_chess(target))

class SkChessBoardScene(sk.Scene):
    def __init__(self, game):
        sk.Scene.__init__(self)
        self.game = game
        self.name = 'GameScene'
        #chess_pieces_dict = self.create_pieces_sprite_dict()
        #for i, piece_name in enumerate(sorted(chess_pieces_dict)):
        #    node = chess_pieces_dict[piece_name]
        #    node.position += ((i+1) * 40, (i+1) * 40)
        #    self.add_child(node)
        self.board_tiles_dict = self.create_board_tiles_dict()
        #print(' '.join([x for x in self.board_tiles_dict]))
        for board_square in self.board_tiles_dict.itervalues():
            self.add_child(board_square)
        chess_pieces_list = self.create_pieces_list()
        #for piece in sorted(self.get_children_with_name('*')):
        #    print(piece.name, piece.frame)
        #self.selected = None
        #self.target_pos = None
        #self.selected_pos = None

    #@classmethod
    #def create_pieces_sprite_dict(cls, piece_types=None):
    #    # return a dictionary of {piece_name : sk_BoardPiece} entries
    #    pieces_dict = {'bishop': 2,
    #                   'king':   1,
    #                   'knight': 2,
    #                   'pawn':   8,
    #                   'queen':  1,
    #                   'rook':   2}
    #    #piece_types = piece_types or 'pawn rook queen king bishop knight'.split()
    #    piece_names = ('{} {} {}'.format(color, ptype, i) for color in ('black', 'white')
    #                                                      for ptype in pieces_dict
    #                                                      for i in xrange(pieces_dict[ptype]))
    #    return {name : sk_ChessPiece(name) for name in piece_names}

    def create_pieces_list(self):
        def make_and_place_piece(piece):
            #print(piece.name)
            gui_piece = sk_ChessPiece(piece)
            #print(piece.coord.as_chess)
            gui_piece.position = self.board_tiles_dict[piece.coord.as_chess].position
            gui_piece.prev_position = gui_piece.position
            self.add_child(gui_piece)
            return gui_piece
        return [make_and_place_piece(piece) for piece
                in self.game.board.get_piece_list()]

    def create_board_tiles_dict(self):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          sk_BoardSquare} entries
        # useful for node hit-testing, greatly simplifies touch_began
        return {tile.as_chess : sk_BoardSquare(tile)
                for tile in self.game.board.tiles}

    def did_change_size(self, old_size):
        pass

    def update(self):
        pass

    def touch_began(self, node, touch):
        pass
        #if node == self:
        #    return
        #node.prev_position = node.position
        #if node is not self:
        #    print(node.__class__, node.name)
        #    node.position = touch.location

    def touch_moved(self, node, touch):
        if node == self:
            return
        node.position = touch.location

    def touch_ended(self, node, touch):
        if node == self:
            return
        for square in self.get_children_with_name('*'):
            if isinstance(square, sk_BoardSquare) and touch in square:
                is_valid = node.is_move_valid(square.name)
                print(node.name, square.name, is_valid)
                if is_valid:
                    node.move(square.name)
                    node.set_position(square.position)
                    sound.play_effect('8ve:8ve-tap-professional')
                    self.game.board.switch_turn()
                else:
                    node.undo_position()
                    sound.play_effect('8ve:8ve-beep-rejected')
                not_str = '' if is_valid else 'not ' 
                print('{} was {}moved to square {}'.format(node.name, not_str, square.name))


if __name__ == '__main__':
    print('=' * 30)
    from SkChessView import SkChessView
    SkChessView()
