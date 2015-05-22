#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import dialogs, os, sk, sound, ui
#from create_pieces_sprite_dict import GameScene
#from Phantom.core.coord.point import Coord
from Phantom.core.exceptions import ChessError, InvalidMove, LogicError
from Phantom.core.pieces import ChessPiece
from Phantom.core.game_class import ChessGame
import Phantom.constants as C

#img_dir = '../gui_pythonista/imgs'
#img_dir = '../images'
img_dir = 'Images'

w, h = ui.get_screen_size()
# globals values are reset in SkChessBoardScene.did_change_size()
square_size = min(w, h) / 8
half_ss = square_size / 2
tile_Size = sk.Size(square_size, square_size)
piece_Size = sk.Size(square_size - 2, square_size - 2)

#print(__name__)

class sk_BoardSquare(sk.SpriteNode):
    #w, h = ui.get_screen_size()
    #s
    #tile_size = sk.Size(C.scale_factor, C.scale_factor)

    def __init__(self, tile):
        sk.SpriteNode.__init__(self) # , sk.Texture(tile.color))
        self.alpha = 0.3
        self.color = tile.tile_color
        self.name = tile.fen_loc  # as_chess
        # invert y because board goes top to bottom but
        #                     sk goes bottom to top
        self.position = (tile.x * square_size + half_ss,
                   (7 - tile.y) * square_size + half_ss)
        self.size = tile_Size
        #x = tile.x * square_size
        #y = tile.y * square_size
        #half_ss = square_size /2
        #print(square_size, half_ss)
        #self.position = (x+half_ss, y+half_ss)  # magic numbers!!
        #self.size = sk.Size(square_size, square_size)

    def __contains__(self, touch_or_point):  # if touch in sk_BoardSquare
        try:
            return self.frame.contains_point(touch_or_point.location)
        except AttributeError:
            return self.frame.contains_point(touch_or_point)


class sk_ChessPiece(sk.SpriteNode):
    fmt = os.path.join(img_dir, 'Chess set images {}.jpg')
    #piece_size = sk.Size(square_size-2, square_size-2)

    def __init__(self, piece):
        assert piece and isinstance(piece, ChessPiece)
        #piece_name = piece_name or 'white queen'
        #piece_name = piece_name.rpartition(' ')[0]  # white queen 0 --> white queen
        #print(os.d, self.fmt.format(piece_name))
        #print(self.fmt.format(piece.name))
        sk.SpriteNode.__init__(self, sk.Texture(self.fmt.format(piece.name)))
        self.alpha = 0.5
        self.piece = piece
        #self.name = piece_name
        self.size = piece_Size
        #self.prev_position = self.position
        self.touch_enabled = True

    @property
    def fen_loc(self):
        return self.piece.fen_loc

    @property
    def name(self):
        return self.piece.name

    #def touch_began(self, node, touch):
    #    print('touch_began({}, {}, {})'.format(self, node, touch))
    #    self.prev_position = self.position

    # this is not a setter because we want touch_moved() and
    # touch_ended() to set position without setting prev_position
    #def set_position(self, position):
    #    self.prev_position = self.position = position

    #def undo_position(self):
    #    self.position = self.prev_position

    #def is_move_valid(self, target):
    #    print('is_move_valid({})'.format(target))
    #    return self.piece.is_move_valid(target)

    def move(self, target):
        assert C.is_valid_fen_loc(target)
        try:
            return self.piece.board.move(self.piece.fen_loc + target)
        except (ChessError, InvalidMove, LogicError) as e:
            dialogs.hud_alert('{}: {}'.format(e.__class__.__name__, e))
        return False
    
    '''
    #@ui.in_background
    def zmove(self, target):
        assert C.is_valid_fen_loc(target)
        save_fen_loc = self.fen_loc
        #print(10, self.piece)
        move_was_made = self.piece.board.move(self.piece.fen_loc + target)
        #print(11, self.piece)
        print('mwm 1', move_was_made)
        move_was_made = save_fen_loc != self.fen_loc
        print('mwm 2', move_was_made)
        if move_was_made:
            self.set_position(self.parent.board_tiles_dict[target].position)
            sound.play_effect('8ve:8ve-tap-professional')
            #self.game.board.switch_turn()
        else:
            self.undo_position()
            sound.play_effect('8ve:8ve-beep-rejected')
        not_str = '' if move_was_made else 'not ' 
        print('{} was {}moved to square {}'.format(save_repr, not_str, target))
        print(repr(self.piece))
        print('')
        '#''
        #return self.piece.move(target)
        #is_valid = node.is_move_valid(square.name)
                #print(node.name, square.name, is_valid)
                save_piece_name = repr(node.piece)
                #if is_valid:
                move_was_made = node.move(square.name)
                print('mwm', move_was_made)
                if move_was_made:
                    node.set_position(square.position)
                    sound.play_effect('8ve:8ve-tap-professional')
                    #self.game.board.switch_turn()
                else:
                    node.undo_position()
                    sound.play_effect('8ve:8ve-beep-rejected')
                not_str = '' if move_was_made else 'not ' 
                print('{} was {}moved to square {}'.format(save_piece_name, not_str, square.name))
                print(repr(node.piece))
                print('')
    '''

class SkChessBoardScene(sk.Scene):
    def __init__(self, game):
        sk.Scene.__init__(self)
        #print(self.frame)
        #square_size = min(self.frame.w, self.frame.h) / 8
        self.game = game
        self.save_position = None
        #self.name = 'GameScene'
        #chess_pieces_dict = self.create_pieces_sprite_dict()
        #for i, piece_name in enumerate(sorted(chess_pieces_dict)):
        #    node = chess_pieces_dict[piece_name]
        #    node.position += ((i+1) * 40, (i+1) * 40)
        #    self.add_child(node)
        self.board_tiles_dict = self.create_board_tiles_dict()
        #print(' '.join([x for x in self.board_tiles_dict]))
        for tile in self.tiles:
            self.add_child(tile)
        chess_pieces_list = self.create_pieces_list()
        #for piece in sorted(self.get_children_with_name('*')):
        #    print(piece.name, piece.frame)
        #self.selected = None
        #self.target_pos = None
        #self.selected_pos = None

    @property
    def name(self):
        return game.name

    @property
    def tiles(self):
        return self.board_tiles_dict.itervalues()

    def create_board_tiles_dict(self):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          sk_BoardSquare} entries
        # useful for node hit-testing, greatly simplifies touch_began
        return {tile.fen_loc : sk_BoardSquare(tile)
                for tile in self.game.board.tiles}

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
            gui_piece.position = self.board_tiles_dict[piece.fen_loc].position
            gui_piece.prev_position = gui_piece.position
            self.add_child(gui_piece)
            return gui_piece
        return [make_and_place_piece(piece) for piece
                in self.game.board.get_piece_list()]

    def create_board_tiles_dict(self):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          sk_BoardSquare} entries
        # useful for node hit-testing, greatly simplifies touch_began
        return {tile.fen_loc : sk_BoardSquare(tile)
                for tile in self.game.board.tiles}

    def did_change_size(self, old_size):
        print('did_change_size: {} --> {}'.format(old_size, self.size))
        w, h = ui.get_screen_size()
        global square_size, half_ss, tile_Size, piece_Size
        square_size = min(w, h) / 8
        half_ss = square_size / 2
        tile_Size = sk.Size(square_size, square_size)
        piece_Size = sk.Size(square_size - 2, square_size - 2)
        #pass

    def update(self):
        pass

    def touch_began(self, node, touch):
        if node == self:
            return
        self.save_position = node.position
        #pass
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
            #print(square.name)
            if isinstance(square, sk_BoardSquare) and touch in square:
                target_fen_loc = square.name
                #is_valid = node.is_move_valid(square.name)
                #print(node.name, square.name, is_valid)
                
                #target_piece = self.board.pieces_dict.get(target, None)
                #if is_valid:
                save_fen_loc = node.fen_loc
                #node.move() is called on a different thread so it returns None!!!
                move_was_made = node.move(target_fen_loc) # always returns None!!
                #print('mwm 1', move_was_made)  # fails!!
                move_was_made = node.fen_loc != save_fen_loc
                #print('mwm 2', move_was_made)
                if move_was_made:
                    for piece in self.get_children_with_name('*'):
                        # remove the killed sk_ChessPiece
                        if (piece != node
                        and isinstance(piece, sk_ChessPiece)
                        and piece.fen_loc == node.fen_loc):
                            if piece.piece.ptype == 'king':
                                import dialogs
                                dialogs.hud_alert('Game over man!')
                            piece.remove_from_parent()
                    node.position = square.position
                    sound.play_effect('8ve:8ve-tap-professional')
                else:
                    node.position = self.save_position
                    sound.play_effect('8ve:8ve-beep-rejected')
                not_str = '' if move_was_made else 'not '
                fmt = '{} at {} was {}moved to square {}'
                print(fmt.format(node.name, save_fen_loc, not_str, square.name))
                #print(repr(node.piece))
                print('')

if __name__ == '__main__':
    print('=' * 30)
    from SkChessView import SkChessView
    SkChessView()
