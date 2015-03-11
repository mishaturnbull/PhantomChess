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

"""The core of the pieces."""

from Phantom.constants import *
from Phantom.core.chessobj import PhantomObj
from Phantom.core.coord.point import Coord, Grid, bounds
from Phantom.core.exceptions import InvalidMove, InvalidDimension
from Phantom.core.coord.vectored_lists import *
from Phantom.core.coord.dirs import dirfinder
from Phantom.core.players import Side
from Phantom.boardio.boardcfg import Namespace
from Phantom.functions import dist, round_up, round_down
from Phantom.utils.debug import call_trace, log_msg
import uuid

__all__ = []

class ChessPiece (PhantomObj):
    
    allIsFrozen = False  # all piece level freeze
    bounds = bounds
    
    # overwritten by subclasses
    ptype = None
    default_origins = []
    
    def __init__(self, pos, color, owner=None):
        self.color = Side(color)
        if not pos in self.bounds:
            raise InvalidDimension('Piece spawned out of bounds: {}'.format(str(pos)), 
                                   'Phantom.core.pieces.ChessPiece.__init__()')
        self.coord = pos
        self.isFrozen = False  # piece level freeze
        self.promotable = False
        self.firstmove = True
        self._uuid = uuid.uuid4()
        self.fen_char = eval('c_{}_{}'.format(self.color.color, self.ptype))
        if use_unicode:
            self.disp_char = eval('d_{}_{}'.format(self.color.color, self.ptype))
        else:
            self.disp_char = self.fen_char
        self.pythonista_gui_imgname = 'Chess set images {} {}.jpg'.format(self.color.color, self.ptype)
        if owner:
            self.owner = None  # Set the attribute before it can be checked in set_owner()
            self.set_owner(owner)
        else:
            self.owner = None
        self.data = Namespace()
        
        # this cache holds moves that are allowed by the .apply_ruleset() method
        # it will be updated after a move and is used to speed up the .valid() method
        # by shortening the list it must iterate through
        self.subvalidcache = []
        self.subvalidcache = self.update_cache()
    
    def __repr__(self):
        return '<{} at {} in {}>'.format(self.ptype, self.coord, hex(id(self)))
    
    def __hash__(self):
        return int(self._uuid) % (self.owner.moves + 1)
    
    def set_owner(self, owner):
        if self.owner is not None:
            return
        self.owner = owner
        self.owner.add_owned_piece(self)
    
    # This applies the piece's ruleset as described in level 1.1
    def apply_ruleset(self, target):
        return True
    
    # method is only usable after set_owner is used
    def suicide(self):
        self.owner.board.kill(self)
    
    @property
    def image(self):
        return '{}_{}'.format(self.color, self.ptype)
    
    # implementation detail 5
    @call_trace(3)
    def valid(self):
        ret = []
        for pos in self.subvalidcache:
            if self.owner.validatemove(self.coord, pos):
                ret.append(pos)
        return ret
    
    @property
    def is_promotable(self):
        if self.ptype == 'pawn':
            if self.color == 'white':
                if self.coord.y == 7:
                    return True
            if self.color == 'black':
                if self.coord.y == 0:
                    return True
        return False
    
    @call_trace(3)
    def check_target(self, target):
        piece = self.owner.board[target]
        if (piece == []) or (piece is None):
            log_msg('check_target: target is None, True', 5)
            ret = True
        elif piece.color == self.color:
            log_msg('check_target: target is same color, False', 5)
            ret = False
        else:
            log_msg('check_target: unknown, True', 5)
            ret = True
        return ret
    
    @call_trace(3)
    def check_path(self, path):
        for pos in path[:-1]:
            piece = self.owner.board[pos]
            if not ((piece == []) or (piece is None)):
                return False
        return True

    @call_trace(3)
    def path_to(self, target):
        start = self.coord
        end = target
        dir = dirfinder(self, target)
        dist_to = int(round_down(dist(self.coord, target)))
        path = dir[1](self)
        squares = path[:dist_to]
        return squares
    
    @call_trace(2)
    def is_move_valid(self, target):
        if target not in bounds:
            return False
        does_follow_rules = self.apply_ruleset(target)
        is_valid_target = self.check_target(target)
        path = self.path_to(target)
        is_clear_path = self.check_path(path)
        is_turn = self.owner.is_turn()
        return does_follow_rules and is_valid_target and is_clear_path and is_turn
    
    @staticmethod
    def type_from_chr(chr):
        if chr in ('p', 'P'):
            return Pawn
        elif chr in ('r', 'R'):
            return Rook
        elif chr in ('n', 'N'):
            return Knight
        elif chr in ('b', 'B'):
            return Bishop
        elif chr in ('k', 'K'):
            return King
        elif chr in ('q', 'Q'):
            return Queen
    
    @call_trace(3)
    def threatens(self):
        moves = self.valid()
        pieces = []
        for move in moves:
            piece = self.owner.board[move]
            if piece is not None:
                pieces.append(piece)
        return pieces
    
    @call_trace(3)
    def threatened_by(self):
        moves = self.owner.board.all_legal()
        pieces = []
        for piece in moves:
            if piece is self or piece.color == self.color:
                continue
            else:
                if self.coord in piece.valid():
                    pieces.append(piece)
        return pieces
    
    @call_trace(2)
    def move(self, target):
        self.owner.board.kill(self.owner.board[target])
        self.coord = target
        self.subvalidcache = self.update_cache()
        self.firstmove = False
    
    @call_trace(4)
    def update_cache(self):
        ret = []
        for tile in self.owner.board.tiles:
            if self.apply_ruleset(tile.coord):
                ret.append(tile.coord)
        return ret
        
__all__.append('ChessPiece')

# Individual piece subtypes

class Pawn (ChessPiece):
    
    ptype = 'pawn'
    default_origins = [Coord(x, y) for x in range(grid_width) for y in (1, 6)]
    tests = [Coord(1, 1), Coord(-1, 1)]
    
    @call_trace(40)
    def apply_ruleset(self, target):
        if self.color == 'white':
            op = lambda a, b: a + b
        elif self.color == 'black':
            op = lambda a, b: a - b
        
        allowed = [Coord(self.coord.x, op(self.coord.y, 1))]
        if self.firstmove:
            allowed.append(Coord(self.coord.x, op(self.coord.y, 2)))
        tests = [op(self.coord, self.tests[0]), op(self.coord, self.tests[1])]
        for test in tests:
            if self.owner.board[test] is not None:
                allowed.append(test)
            
        ret = target in allowed
        
        if self.owner.board.en_passant_rights == '-':
            self.owner.board.data['move_en_passant'] = False
        elif Coord.from_chess(self.owner.board.en_passant_rights) in tests:
            self.owner.board.data['move_en_passant'] = True
            ret = True
        else:
            self.owner.board.data['move_en_passant'] = False
        
        return ret
    
    # The reason for overriding this method is that the pawns, after moving,
    # may *not* have en passant rights or other weird things that pawns can do
    # These would not be included in the .subvalidcache list and therefore not 
    # displayed on the GUI as valid moves
    def valid(self):
        self.subvalidcache = self.update_cache()
        ret = []
        for p in self.subvalidcache:
            if self.owner.validatemove(self.coord, p):
                ret.append(p)
        return ret

__all__.append('Pawn')

class Rook (ChessPiece):
    
    ptype = 'rook'
    default_origins = [Coord(x, y) for x in (0, 7) for y in (0, 7)]
    
    @call_trace(40)
    def apply_ruleset(self, target):
        allowed = []
        allowed.extend(north(self))
        allowed.extend(south(self))
        allowed.extend(east(self))
        allowed.extend(west(self))
        return target in allowed
__all__.append('Rook')

class Bishop (ChessPiece):
    
    ptype = 'bishop'
    default_origins = [Coord(x, y) for x in (2, 5) for y in (0, 7)]
    
    @call_trace(40)
    def apply_ruleset(self, target):
        allowed = []
        allowed.extend(ne(self))
        allowed.extend(nw(self))
        allowed.extend(se(self))
        allowed.extend(sw(self))
        return target in allowed
__all__.append('Bishop')

class Queen (ChessPiece):
    
    ptype = 'queen'
    default_origins = [Coord(3, y) for y in (0, 7)]
    
    @call_trace(40)
    def apply_ruleset(self, target):
        allowed = []
        allowed.extend(north(self))
        allowed.extend(south(self))
        allowed.extend(east(self))
        allowed.extend(west(self))
        allowed.extend(ne(self))
        allowed.extend(nw(self))
        allowed.extend(se(self))
        allowed.extend(sw(self))
        return target in allowed
__all__.append('Queen')

class King (ChessPiece):
    
    ptype = 'king'
    default_origins = [Coord(4, y) for y in (0, 7)]
    
    @call_trace(40)
    def _apply_ruleset(self, target):
        if round_down(dist(self.coord, target)) == 1:
            return True
        return False

    @call_trace(40)
    def apply_ruleset(self, target):
        if not self.owner.board.cfg.do_checkmate:
            return self._apply_ruleset(target)
        empty_board = self._apply_ruleset(target)  # could move if there were no pieces on the board
        other_allowed = []
        self.owner.board.set_checkmate_validation(False)  # avoid recursion
        for piece in self.owner.board.pieces:
            if piece is self or piece.color == self.color:
                continue
            else:
                other_allowed.extend(piece.valid())
        self.owner.board.set_checkmate_validation(True)
        if target in other_allowed:
            return False
        else:
            return empty_board
__all__.append('King')

class Knight (ChessPiece):
    
    ptype = 'knight'
    default_origins = [Coord(x, y) for x in (1, 6) for y in (0, 7)]
    
    @call_trace(40)
    def apply_ruleset(self, target):
        allowed = [self.coord + Coord(1, 2),
                   self.coord + Coord(2, 1),
                   self.coord + Coord(2, -1),
                   self.coord + Coord(1, -2),
                   self.coord - Coord(1, 2),
                   self.coord - Coord(2, 1),
                   self.coord - Coord(2, -1),
                   self.coord - Coord(1, -2)]
        for pos in allowed:
            if not ((grid_height > pos.y >= 0) and (grid_width > pos.x >= 0)):
                allowed.remove(pos)
        return target in allowed
    
    @call_trace(40)
    # override this method for two reasons:
    # A. knights can jump over pieces so this is irrevelent
    # B. the path generator doesn't work properly for the knight's direction of movement
    #    and this saves having to implement special-case code in the ChessPiece.path_to method
    def path_to(self, target):
        return [0]
__all__.append('Knight')

