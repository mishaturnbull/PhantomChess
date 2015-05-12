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

"""Squares in a given direction."""

from Phantom.core.coord.point import Coord
from Phantom.constants import grid_height, grid_width
from Phantom.utils.decorators import integer_args
from Phantom.utils.debug import call_trace

__all__ = []

# implementation detail 2, 3

# 671: why is integer_args being applied here?  these functions will never have an argument
#      other than a piece object which cannot be converted to a single integer

@call_trace(9)
@integer_args
def north(piece):
    x, y = piece.coord
    return [Coord(x, i) for i in xrange(y+1, grid_height)]

@call_trace(9)
@integer_args
def south(piece):
    x, y = piece.coord
    return [Coord(x, i) for i in xrange(y-1, -1, -1)]

@call_trace(9)
@integer_args
def east(piece):
    x, y = piece.coord
    return [Coord(i, y) for i in xrange(x+1, grid_width)]

@call_trace(9)
@integer_args
def west(piece):
    x, y = piece.coord
    return [Coord(i, y) for i in xrange(x-1, -1, -1)]

@call_trace(9)
@integer_args
def ne(piece):
    x, y = piece.coord
    iterto = min(grid_width-x, grid_height-y)
    return [Coord(x+i, y+i) for i in xrange(1, iterto)]

@call_trace(9)
@integer_args
def se(piece):
    x, y = piece.coord
    iterto = min(grid_width-x, y)
    return [Coord(x+i, y-i) for i in xrange(1, iterto+1)]

@call_trace(9)
@integer_args
def nw(piece):
    x, y = piece.coord
    iterto = min(x, grid_height-y)
    return [Coord(x-i, y+i) for i in xrange(1, iterto+1)]

@call_trace(9)
@integer_args
def sw(piece):
    x, y = piece.coord
    iterto = min(x, y)
    return [Coord(x-i, y-i) for i in xrange(1, iterto+1)]

@call_trace(9)
@integer_args
def unknown(piece):
    def join(*args):
        ret = []
        for arg in args:
            ret.extend(arg(piece))
        return ret
    known = join(north, south, east, west, ne, se, nw, sw)
    alltiles = piece.owner.board.tiles
    all = [tile.coord for tile in alltiles]
    return [c for c in all if not c in known]

__all__ = [func.__name__ for func in (north, south, east, west, ne, se, nw, sw, unknown)]

def to_alpha(coord_list):
    print(coord_list)
    try:
        return [x.as_chess for x in coord_list]
    except KeyError as e:
        return [str(e)]

if __name__ == '__main__':
    print('=' * 20)
    import string
    class SimplePiece(object):
        cols = 'abcdefgh'  #  west --> east
        rows = '12345678'  # south --> north
        
        def __init__(self, fen_char='p', fen_loc='d4'):
            self.fen_char = fen_char
            self.fen_loc  = fen_loc

        def __str__(self):  ''
            return '{} @ {} ({})'.format(self.fen_char, self.fen_loc, self.coord)
        
        @property
        def col(self):
            return self.fen_loc[0]

        @property
        def row(self):
            return self.fen_loc[1]
        
        def has_valid_loc(self):
            return self.col in self.cols and self.row in self.rows

        @property
        def coord(self):
            return Coord.from_chess(self.fen_loc)

        @property
        def north_part(self):  # 'd4' --> '5678'
            return self.rows.partition(self.row)[2]

        @property
        def south_part(self):  # 'd4' --> '321'
            return reversed(self.rows.partition(self.row)[0])

        @property
        def east_part(self):   # 'd4' --> 'efgh'
            return self.cols.partition(self.col)[2]

        @property
        def west_part(self):   # 'd4' --> 'cba'
            return reversed(self.cols.partition(self.col)[0])

        def north(self):
            print('north>' + ' '.join(to_alpha(north(self))))
            fmt = '{}{}'.format(self.col, '{}')
            return (fmt.format(x) for x in self.north_part)
        
        def south(self):
            print('south>' + ' '.join(to_alpha(south(self))))
            fmt = '{}{}'.format(self.col, '{}')
            return (fmt.format(x) for x in self.south_part)

        def east(self):
            print(' east>' + ' '.join(to_alpha(east(self))))
            fmt = '{}{}'.format('{}', self.row)
            return (fmt.format(x) for x in self.east_part)
            
        def west(self):
            print(' west>' + ' '.join(to_alpha(west(self))))
            fmt = '{}{}'.format('{}', self.row)
            return (fmt.format(x) for x in self.west_part)

        def ne(self):
            print('   ne>' + ' '.join(to_alpha(ne(self))))
            return (y+x for x,y in zip(self.north_part, self.east_part))

        def se(self):
            print('   se>' + ' '.join(to_alpha(se(self))))
            return (y+x for x,y in zip(self.south_part, self.east_part))

        def nw(self):
            print('   nw>' + ' '.join(to_alpha(nw(self))))
            return (y+x for x,y in zip(self.north_part, self.west_part))

        def sw(self):
            print('   sw>' + ' '.join(to_alpha(sw(self))))
            return (y+x for x,y in zip(self.south_part, self.west_part))

        def dir_finder(self, target):
            """Locate the direction in which the target lies and return a 2-tuple of:
            (the string of the direction, the function that gives it)"""
            for func in (self.north, self.south, self.east, self.west,
                            self.ne, self.nw, self.se, self.sw):
                if target in func():
                    return func.__name__, func
            return ('unknown', lambda p: [0])

    my_piece = SimplePiece('p', 'h8')
    
    print('*' * 20)
    print(my_piece, my_piece.rows, my_piece.cols)

    print('north', ' '.join(my_piece.north()))
    print('south', ' '.join(my_piece.south()))
    print(' east', ' '.join(my_piece.east()))
    print(' west', ' '.join(my_piece.west()))
    print('')
    print('   ne', ' '.join(my_piece.ne()))
    print('   se', ' '.join(my_piece.se()))
    print('   nw', ' '.join(my_piece.nw()))
    print('   sw', ' '.join(my_piece.sw()))
