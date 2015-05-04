#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import os, sk
from Phantom.core.coord.point import Coord
from Phantom.core.game_class import ChessGame
import Phantom.constants as C

img_dir = '../gui_pythonista/imgs'

class GameScene(sk.Scene):
    def __init__(self, game):
        sk.Scene.__init__(self)
        self.game = game
        self.name = 'GameScene'
        chess_pieces_dict = self.create_pieces_sprite_dict()
        for i, piece_name in enumerate(sorted(chess_pieces_dict)):
            node = chess_pieces_dict[piece_name]
            node.name = piece_name
            node.position += ((i+1) * 80, 20 + (i+1) * 50)
            node.alpha = 0.5
            self.add_child(node)
        board_tiles_dict = self.create_board_tiles_dict()
        for board_square in board_tiles_dict.itervalues():
            self.add_child(board_square)
        for piece in sorted(self.get_children_with_name('*')):
            print(piece.name, piece.frame)
        self.selected = None
        self.target_pos = None
        self.selected_pos = None

    @classmethod
    def create_pieces_sprite_dict(cls, piece_types=None):
        # returns a dict of {piece_name : piece_as_sk.SpriteNode} entries
        fmt = os.path.join(img_dir, 'Chess set images {}.jpg')
        def make_piece_sprite(piece_name):
            piece_sprite = sk.SpriteNode(sk.Texture(fmt.format(piece_name)))
            piece_sprite.name = piece_name
            piece_sprite.alpha = 0.5
            return piece_sprite
        # returns a dict of {piece_short_name : piece_as_sk.SpriteNode} entries
        piece_types = piece_types or 'pawn rook queen king bishop knight'.split()
        piece_names = ('{} {}'.format(color, ptype) for ptype in piece_types
                                                    for color in ('black', 'white'))
        fmt = os.path.join(img_dir, 'Chess set images {}.jpg')
        return {piece_name : make_piece_sprite(piece_name)
                             for piece_name in piece_names}

    def create_board_tiles_dict(self):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          colored_square_as_sk.SpriteNode}
        # useful for node hit-testing,much simplifies touch_began
        tile_size = sk.Size(C.scale_factor, C.scale_factor)
        def make_board_tile(tile):
            node = sk.SpriteNode()
            node.name = str(tile.coord.as_chess)
            node.size = tile_size
            node.alpha = 0.3
            pos = tile.coord.as_screen
            node.position = (pos.x, pos.y)
            node.color = tile.tilecolor
            return node
        return {tile.coord : make_board_tile(tile)
                for tile in self.game.board.tiles}

    def did_change_size(self, old_size):
        pass

    def update(self):
        pass

    def touch_began(self, node, touch):
        pass

    def touch_moved(self, node, touch):
        pass

    def touch_ended(self, node, touch):
        pass


class GameView(sk.View):
    def __init__(self, game=None):
        self.game = game or ChessGame()
        sk.View.__init__(self, GameScene(self.game))
        self.shows_fps = True
        self.present()


def main():
    print('=' * 30)
    GameView()
    #game = ChessGame()
    #game_scene = GameScene(game)
    #scene_view = sk.View(game_scene)
    #scene_view.shows_fps = True
    #scene_view.present()

if __name__ == '__main__':
    main()
