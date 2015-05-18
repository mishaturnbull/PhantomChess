# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

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

import Phantom.constants as C
from Phantom.utils.debug import call_trace, log_msg

import itertools
import uuid

__all__ = []

'''
def xy_from_fen_loc(fen_loc):
    assert is_valid_fen_loc(fen_loc)
    x, y = fen_loc
    return x_chars.index(x), y_chars.index(y)
'''

class ChessPiece(): # (PhantomObj):
    # overwritten by subclasses
    ptype = None
    default_origins = []
    
    #@classmethod
    #def is_valid_fen_loc(cls, fen_loc):
    #    return (fen_loc[0] in C.col_chars
    #        and fen_loc[1] in C.row_chars)

    def __init__(self, owner, fen_loc):
        self.owner = owner
        self.fen_loc = fen_loc
        #print(self.x, self.y)
        #self.x = self.y = 'dude'
        #print(self.x, self.y)
        #print(self.board)
        #print(self.color)
        #print(self.col+self.row)
        #print(type(self.x), type(self.y))
        #print(self.fen_loc, self.x, self.y, C.fen_loc_from_xy(self.x, self.y), C.xy_from_fen_loc(fen_loc))
        #if pos not in self.bounds:
        #    raise InvalidDimension('Piece spawned out of bounds: {}'.format(pos),
        #                           'Phantom.core.pieces.ChessPiece.__init__()')
        #self.coord = pos
        #self.color = color
        #self.name = '{} {}'.format(self.color, self.ptype).lower()
        as_ascii, as_unicode = C.piece_chars[self.name]
        self.fen_char = as_ascii
        self.disp_char = as_unicode if C.use_unicode else as_ascii
        #self.pythonista_gui_img_name = 'Chess set images {}.jpg'.format(self.name)
        #freeze: self.isFrozen = False  # piece level freeze
        self.promotable = False
        self.first_move = True
        self._uuid = uuid.uuid4()
        #self.owner = None  # Set the attribute before it can be checked in set_owner()
        #if owner:
        #    self.set_owner(owner)
        self.data = dict()

        # this cache holds moves that are allowed by the .apply_ruleset() method
        # it will be updated after a move and is used to speed up the .valid() method
        # by shortening the list it must iterate through
        #! self.subvalid_cache = self.update_cache()  FIXME!
        self.subvalid_cache = []

    @property
    def board(self):
        return self.owner.board
        
    @property
    def color(self):
        return self.owner.color

    @property
    def name(self):
        return '{} {}'.format(self.color, self.ptype).lower()

    @property
    def col(self):
        return self.fen_loc[0]

    @property
    def row(self):
        return self.fen_loc[1]

    @property
    def x(self):
        #_x, _y = self.fen_loc
        #print('x:', _x, self.col)
        #assert _x == self.col
        return C.x_chars.index(self.col)

    @property
    def y(self):
        #_x, _y = self.fen_loc
        #print('y:', _y, self.row)
        #assert _y == self.row
        return C.y_chars.index(self.row)

# 671: @ccc you were right in commit 79e3218 - __str__ causes loops
    def as_str(self):
        valid = [c.as_chess for c in self.valid()]
        threatens_fmt = '{} at {}'
        threatens = [threatens_fmt.format(p.ptype, p.fen_char)
                                          for p in self.threatens()]
        threats_fmt = '{} at {}'
        threats = [threats_fmt.format(p.ptype, p.fen_char)
                                      for p in self.threatened_by()]
        return """    {}
    Valid moves: {}
    Is promotable: {}
    This piece threatens: {}
    This piece is threatened by: {}
    """.format(repr(self), valid, self.promotable, threatens, threats)

    def __repr__(self):
        fmt = '<{} at {} ({}, {}) in {}>'
        return fmt.format(self.name, self.fen_loc, self.x, self.y, hex(id(self)))

    def __hash__(self):
        return int(self._uuid) % (self.owner.moves + 1)

    @property
    def as_chess(self):
        return '{} @ {}'.format(self.fen_char, self.fen_loc)

    def friend_or_foe(self, target):
        occupant = self.board[target]
        if occupant:
            return 'friend' if occupant.color == self.color else 'foe'
        else:
            return None

    #@property
    #def as_screen(self):
    #    return self.coord.as_screen

    #def set_owner(self, owner):
    #    if not self.owner:
    #        self.owner = owner
    #        self.owner.add_owned_piece(self)

    # This applies the piece's ruleset as described in level 1.1
    def apply_ruleset(self, target):
        return True

    # method is only usable after set_owner is used
    def suicide(self):
        self.board.kill(self)

    @property
    def image(self):
        return '{}_{}'.format(self.color, self.ptype)

    # implementation detail 5
    @call_trace(3)
    def valid(self):
        return [pos for pos in self.subvalid_cache if self.owner.validatemove(self.coord, pos)]

    # 671: should this be a property or a function?  Does it even matter?
    # ccc: property.  but perhaps only a property of Pawns
    @property
    def is_promotable(self):
        """Tests if a piece is promotable."""
        if self.ptype != 'pawn':
            return False
        return ((self.color == 'white' and self.row == '8')
             or (self.color == 'black' and self.row == '1'))

    @call_trace(3)
    def check_target(self, target):
        """See if a target is valid.  Does not perform full move validation."""
        piece = self.board[target]
        if not piece:
            log_msg('check_target: target is None, True', 5)
            ret = True
        elif piece.color == self.color:
            log_msg('check_target: target is same color, False', 5)
            ret = False
        else:
            log_msg('check_target: unknown, True', 5)
            ret = True
        return ret

    '''
    @call_trace(3)
    def check_path(self, path):
        """Check to see if a given path is clear."""
        for pos in path[:-1]:
            piece = self.board[pos]
            if piece:
                return False
        return True

    # TODO: make this work properly (sometimes it overshoots the target)
    # 671: this seems to work on all pieces except the bishops, would an
    #      iterative process be better:
    #    pdir = dirfinder(self, target)
    #    i = self.coord.__copy__()
    #    ret = []
    #    while not self.board[target]:
    #        i += some other coord at a dist of one in the correct direction
    #        ret.append(i)
    #    return ret

    # @ccc pointed out in issue #49 that a piece at (7, 7) has pieces to southeast
    #      and northwest, neither of which is correct.
    @call_trace(3)
    def path_to(self, target):
        """Generate a path to a target."""
        pdir = self.dir_finder(target)                        # get the direction to target
        dist_to = int(round_down(dist(self.coord, target)))   # determine distance to target
        path = pdir[1](self)                                  # get list of squares in target direction
        squares = path                                        # copy list
        while len(squares) > dist_to:                         # shrink list iteratively until len(squares) == dist_to
            squares = squares[:-1]                            # shrink list iteratively until len(squares) == dist_to
        return squares                                        # return list
    '''
    
    @call_trace(3)
    def clear_path_to_target(self, target):
        pdir = self.dir_finder(target)  # get the direction to target
        if not pdir:
            return False                # you can not get there
        for fen_loc in pdir[1]():       # pdir is ['north', north()]
            if fen_loc == target:
                return True             # target was reached
            if self.board[fen_loc]:
                return False            # another piece is in the way

    @call_trace(2)
    def is_move_valid(self, target):
        if not self.owner.is_turn():
            return False  # fast fail!
        #print('{}.is_move_valid({}) {}'.format(self.__class__.__name__, target, type(target)))
        """Test if the piece is allowed to move to a new specified position."""
        #if target not in bounds:
        if not C.is_valid_fen_loc(target):
            return False
        does_follow_rules = self.apply_ruleset(target)
        is_valid_target = self.check_target(target)
        #path = self.path_to(target)
        #is_clear_path = self.check_path(path)
        is_clear_path = self.clear_path_to_target(target)
        return does_follow_rules and is_valid_target and is_clear_path

    @staticmethod
    def type_from_chr(p_chr):
        """Get the piece class from a SAN character."""
        # 671: updated to use characters defined in PhantomConfig.cfg
        piece_dict = {C.piece_chars['black pawn'][0]: Pawn,
                      C.piece_chars['black rook'][0]: Rook,
                      C.piece_chars['black knight'][0]: Knight,
                      C.piece_chars['black bishop'][0]: Bishop,
                      C.piece_chars['black queen'][0]: Queen,
                      C.piece_chars['black king'][0]: King}
        return piece_dict.get(p_chr.lower(), None)

    @call_trace(3)
    def threatens(self):
        """List the pieces that this piece could kill."""
        return [self.board[move] for move in self.valid() if self.board[move]]

    @call_trace(3)
    def threatened_by(self):
        """List the pieces that could kill this piece."""
        return [piece for piece in self.board.all_legal()
                if piece.color != self.color and self.coord in piece.valid()]

    #@call_trace(2)
    #def move(self, target):
    #    """Go somewhere."""
    #    self.board.kill(self.board[target])
    #    self.coord = target
    #    self.subvalid_cache = self.update_cache()
    #    self.first_move = False

    @call_trace(4)
    def update_cache(self):
        """Return an updated subvalid cache."""
        return [tile.fen_loc for tile in self.board.tiles if self.apply_ruleset(tile.fen_loc)]

    @property
    def north_part(self):  # 'd4' --> '5678'
        return reversed(C.y_chars.partition(self.row)[0])

    @property
    def south_part(self):  # 'd4' --> '321'
        return C.y_chars.partition(self.row)[2]

    @property
    def east_part(self):   # 'd4' --> 'efgh'
        return C.x_chars.partition(self.col)[2]

    @property
    def west_part(self):   # 'd4' --> 'cba'
        return reversed(C.x_chars.partition(self.col)[0])

    # the following functions are generators to improve performance
    def north(self):
        fmt = '{}{}'.format(self.col, '{}')
        return (fmt.format(x) for x in self.north_part)
        
    def south(self):
        fmt = '{}{}'.format(self.col, '{}')
        return (fmt.format(x) for x in self.south_part)

    def east(self):
        fmt = '{}{}'.format('{}', self.row)
        return (fmt.format(x) for x in self.east_part)
            
    def west(self):
        fmt = '{}{}'.format('{}', self.row)
        return (fmt.format(x) for x in self.west_part)

    def ne(self):
        return (y+x for x,y in zip(self.north_part, self.east_part))

    def se(self):
        return (y+x for x,y in zip(self.south_part, self.east_part))

    def nw(self):
        return (y+x for x,y in zip(self.north_part, self.west_part))

    def sw(self):
        return (y+x for x,y in zip(self.south_part, self.west_part))

    def dir_finder(self, target):
        """Locate the direction in which the target lies and return a 2-tuple of:
        (the string of the direction, the function that gives it)"""
        for func in (self.north, self.south, self.east, self.west,
                        self.ne, self.nw, self.se, self.sw):
            if target in func():
                return func.__name__, func
        return None

__all__.append('ChessPiece')

# Individual piece subtypes

class Pawn (ChessPiece):

    ptype = 'pawn'
    #default_origins = [Coord(x, y) for x in range(C.grid_width) for y in (1, 6)]
    #default_originz = 'a2 b2 c2 d2 e2 f2 g2 h2 a7 b7 c7 d7 e7 f7 g7 h7'.split()
    default_origins = [x+'2' for x in C.x_chars] + [x+'7' for x in C.x_chars]
    #assert default_origins == default_originz
    #y = '2' if self.color == 'white' else '7'
    #default_origins = [x+y for x in C.x_chars]
        

    #tests = [Coord(1, 1), Coord(-1, 1)]

    def __init__(self, owner, fen_loc):
        ChessPiece.__init__(self, owner, fen_loc)
        default_row = '2' if self.color == 'white' else '7'
        self.en_passant_rights = self.row == default_row

    @call_trace(4)
    def apply_ruleset(self, target):
        forward_steps = 2 if self.en_passant_rights else 1
        if self.color == 'white':
            allowed = list(self.north())[:forward_steps]
            diagonal_kills = list(self.ne())[:1] + list(self.nw())[:1]
        else:
            allowed = list(self.south())[:forward_steps]
            diagonal_kills = list(self.sw())[:1] + list(self.se())[:1]
        allowed = [x for x in allowed if not self.friend_or_foe(x)]
        for diagonal_kill in diagonal_kills:
            if self.friend_or_foe(diagonal_kill) == 'foe':
                allowed.append(diagonal_kill)
        print('{}.apply_ruleset({}) --> {}'.format(self, target, allowed))
        return target in allowed
        '''
        
        
        if self.color == 'white':
            op = lambda a, b: a + b
        elif self.color == 'black':
            op = lambda a, b: a - b

        allowed = [Coord(self.x, op(self.y, 1)).as_chess]
        if self.first_move:
            allowed.append(Coord(self.x, op(self.y, 2)).as_chess)
        print(allowed)
        for move in allowed:
            piece = self.board.pieces_dict.get(move, None)
            if piece and piece.color == self.color:
            #if move in self.board.pieces_dict:
                allowed.remove(move)
        tests = [op(self.zcoord, self.tests[0]), op(self.zcoord, self.tests[1])]
        for test in tests:
            if test.as_chess in self.board.pieces:
                allowed.append(test.as_chess)

        ret = target in allowed

        if self.board.en_passant_rights == '-':
            self.board.data['move_en_passant'] = False
        elif Coord.from_chess(self.board.en_passant_rights) in tests:
            self.board.data['move_en_passant'] = True
            ret = True
        else:
            self.board.data['move_en_passant'] = False

        return ret
    '''

    # The reason for overriding this method is that the pawns, after moving,
    # may *not* have en passant rights or other weird things that pawns can do
    # These would not be included in the .subvalidcache list and therefore not
    # displayed on the GUI as valid moves
    def valid(self):
        self.subvalid_cache = self.update_cache()
        return [p for p in self.subvalid_cache if self.owner.validatemove(self.coord, p)]

__all__.append('Pawn')

class Rook (ChessPiece):

    ptype = 'rook'
    #default_origins = [Coord(x, y) for x in (0, 7) for y in (0, 7)]
    default_origins = 'a1 a8 h1 h8'.split()

    @call_trace(4)
    def apply_ruleset(self, target):
        return (target in self.north()
             or target in self.south()
             or target in self.east()
             or target in self.west())
__all__.append('Rook')

class Bishop (ChessPiece):

    ptype = 'bishop'
    #default_origins = [Coord(x, y) for x in (2, 5) for y in (0, 7)]
    default_origins = 'c1 c8 f1 f8'.split()

    @call_trace(4)
    def apply_ruleset(self, target):
        return (target in self.ne()
             or target in self.nw()
             or target in self.se()
             or target in self.sw())
__all__.append('Bishop')

class Queen (ChessPiece):

    ptype = 'queen'
    #default_origins = [Coord(3, y) for y in (0, 7)]
    default_origins = 'd1 d8'.split()

    @call_trace(4)
    def apply_ruleset(self, target):
        return (target in self.north()
             or target in self.south()
             or target in self.east()
             or target in self.west()
             or target in self.ne()
             or target in self.nw()
             or target in self.se()
             or target in self.sw())
__all__.append('Queen')

class King (ChessPiece):

    ptype = 'king'
    #default_origins = [Coord(4, y) for y in (0, 7)]
    default_origins = 'e1 e8'.split()

    #@call_trace(4)
    #def _apply_ruleset(self, target):
    #    return round_down(dist(self.coord, target)) == 1

    @call_trace(4)
    def apply_ruleset(self, target):
        allowed = [list(func())[:1] for func in (self.north, self.south, self.east, self.west,
                                                 self.ne, self.nw, self.se, self.sw)]
        return [target] in allowed  # allowed is a list of lists
    '''
    return False  # FIXME!!
        if not self.board.cfg.do_checkmate:
            return self._apply_ruleset(target)
        empty_board = self._apply_ruleset(target)  # could move if there were no pieces on the board
        other_allowed = []
        self.board.set_checkmate_validation(False)  # avoid recursion
        for piece in self.board.pieces:
            if piece.color != self.color:
                other_allowed.extend(piece.valid())
        self.board.set_checkmate_validation(True)
        return False if target in other_allowed else empty_board
    '''

__all__.append('King')

class Knight (ChessPiece):

    ptype = 'knight'
    #default_origins = [Coord(x, y) for x in (1, 6) for y in (0, 7)]
    default_origins = 'b1 b8 g1 g8'.split()

    def knight_moves(self):  # front page drivin' news
        print(self)
        the_moves = []
        for x, y in itertools.permutations((-1, 1, -2, 2), 2):
            if abs(x) != abs(y):
                x = self.x + x
                y = self.y + y
                #print('t/f', self.x, self.y, x, y, 0 <= x <= 7 and 0 <= y <= 7)
                if 0 <= x <= 7 and 0 <= y <= 7:
                    #print(x, y, C.x_chars[x] + C.y_chars[y])
                    the_moves.append(C.x_chars[x] + C.y_chars[y])
        #print (self.ptype, [C.fen_loc_from_xy(x, y) for x, y in self.default_origins])
        print('{}.knight_moves: {} ({}, {}) {}'.format(self.__class__.__name__, self, self.x, self.y, the_moves))
        return tuple(the_moves)

    @call_trace(4)
    def apply_ruleset(self, target):
        return target in self.knight_moves()
        #allowed = [self.coord + Coord(1, 2), 
        #           self.coord + Coord(2, 1),
        #           self.coord + Coord(2, -1),
        #           self.coord + Coord(1, -2),
        #           self.coord - Coord(1, 2),
        #           self.coord - Coord(2, 1),
        #           self.coord - Coord(2, -1),
        #           self.coord - Coord(1, -2)]
        #for pos in allowed:
        #    if not (C.grid_height > pos.y >= 0 and C.grid_width > pos.x >= 0):
        #        allowed.remove(pos)
        #return target in allowed

    @call_trace(4)
    # override this method for two reasons:
    # A. knights can jump over pieces so this is irrevelent
    # B. the path generator doesn't work properly for the knight's direction of movement
    #    and this saves having to implement special-case code in the ChessPiece.path_to method
    #def path_to(self, target):
    #    return [0]
    def clear_path_to_target(self, target):
        return True

__all__.append('Knight')


if __name__ == '__main__':
    print('=' * 20)
    from Phantom.core.players import Player
    p = Pawn(Player(None, 'white'), 'a4')
    #print('main_:', p, p.x, p.y)
    #print('main:', p, p.x, p.y, p.col+p.row)
    p.fen_loc = 'b5'
    #print('main:', p, p.x, p.y, p.col+p.row)
