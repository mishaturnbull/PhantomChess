# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

#        1         2         3         4         5         6         7         8
# 345678901234567890123456789012345678901234567890123456789012345678901234567890

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

"""The chessboard itself."""

import Phantom.constants as C
from Phantom.core.chessobj import PhantomObj
from Phantom.core.players import Player
from Phantom.core.exceptions import InvalidMove, LogicError, ChessError
from Phantom.core.pieces import ChessPiece
# from Phantom.core.coord.vectored_lists import north, south, east, west, ne, se, nw, sw
#from Phantom.core.coord.point import Coord
from Phantom.boardio.save import save
from Phantom.boardio.load import load_game
from Phantom.boardio.boardcfg import Cfg
from Phantom.utils.debug import call_trace, log_msg
from Phantom.utils.decorators import exc_catch
from Phantom.functions import round_down, dist
import collections
import contextlib
import uuid

__all__ = []


def load(name):
    fen = load_game(name)
    game = Board(Player('white'), Player('black'), fen)
    game.set_name(name)
    return game
__all__.append('load')


class Tile (PhantomObj):
    isfrozen = False

    def __init__(self, fen_loc, color):
        self.fen_loc = fen_loc
        #self.x = pos.x
        #self.y = pos.y
        #self.color = color
        #self.coord = pos
        if color == 'black':
            self.disp_char = C.black_space_char[int(C.use_unicode)]  # zero or one
        else:
            self.disp_char = C.white_space_char[int(C.use_unicode)]  # zero or one
        self.tile_color = C.grid_colors[color]
        #print(repr(self))
        
        #def __repr__(self):
        #    return '{}({}, {}) ({}, {})'.format(self.__class__.__name__, self.fen_loc,
        #                                        self.tile_color, self.x, self.y)

    def __repr__(self):
        fmt = '<{} {} at {} ({}, {}) in {}>'
        return fmt.format(self.tile_color, self.__class__.__name__, self.fen_loc, self.x, self.y, hex(id(self)))

    @property
    def col(self):
        return self.fen_loc[0]

    @property
    def row(self):
        return self.fen_loc[1]

    @property
    def x(self):
        return C.x_chars.index(self.col)

    @property
    def y(self):
        return C.y_chars.index(self.row)

    #@property
    #def zas_chess(self):
    #    #return self.coord.as_chess
    #    return self.fen_loc

    #@property
    #def as_screen(self):
    #    return self.zcoord.as_screen

    #@property
    #def zcoord(self):
    #    #return self.coord.as_screen
    #    #return Coord.from_chess(self.fen_loc)
    #    return Coord(self.x, self.y)

__all__.append('Tile')

def make_tiles_dict():
    fen_locs = [col+row for col in 'abcdefgh' for row in '12345678']
    #print(' '.join(fen_loc + ('w' if i % 2 else 'b') for i, fen_loc in enumerate(fen_locs)))
    #print(len(list(fen_locs)))
    return {fen_loc: Tile(fen_loc, ('white' if i % 2 else 'black'))
            for i, fen_loc in enumerate(fen_locs)}
    #tiles_dict = collections.OrderedDict()  # is OrderedDict useful??
    #for fen_loc in (col+row for col in cols for row in rows):
    #    tiles_dict[fen_loc] = Tile(fen_loc, color)
    #    color = self.opcolor(color)
    #return tiles_dict

def _make_pieces_dict(fen_str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
    # returns a dict of {fen_str : fen_char} entries like {'e8': 'k'}
    pieces_dict = collections.OrderedDict()
    for y, row_fen in enumerate(fen_str.split('/')):
        x = 0
        for c in row_fen:
            if c.isdigit():
                x += int(c)
            else:
                fen_loc = C.x_chars[x] + C.y_chars[y]
                #print(fen_loc, C.xy_from_fen_loc(fen_loc), c)
                pieces_dict[fen_loc] = c
                x += 1
    return pieces_dict

class Board (PhantomObj):
    isfrozen = False  # is the board frozen?
    movenum = 0       # how many moves have been made

    #@classmethod
    #def is_valid_fen_loc(cls, fen_loc):
    #    return (fen_loc[0] in C.x_chars
    #        and fen_loc[1] in C.y_chars)

    #@classmethod
    #def fen_loc_from_xy(x, y):
    #    try:
    #        return C.col_chars[y] + C.row_chars[x]
    #    except IndexError:
    #        return None

    @classmethod
    def op_color(cls, color):
        for c in C.colors:
            if c != color:
                return c
        assert False, 'Should never happen!'

    def __init__(self, chess_game, fen_str=None, **cfgkws):
        self.game = chess_game
        self.fen_str = fen_str or C.opening_fen
        self.players_dict = {x : Player(self, x) for x in C.colors}
        self.tiles_dict = make_tiles_dict()
        #p1=Player('white'), p2=Player('black'), fen=C.opening_fen, **cfgkws):
        
        #self.players = [Player(self, 'white'), Player(self, 'black')]
        #self.pieces = set()
        self.dead = set()
        self.name = 'New Game'
        self.cfg = Cfg(**cfgkws)
        self.cfg.set_board(self)
        #self.game = None
        self.lastmove = (None, None)
        self._uuid = uuid.uuid4()
        self.data = dict()
        self.start_pos = self.fen_str

        #tile_color = 'black'
        #op_color = lambda c: 'white' if c == 'black' else 'black'
        #self.tiles = set()
        #for x in range(C.grid_width):
        #    for y in range(C.grid_height):
        #        self.tiles.add(Tile(Coord(x, y), tile_color))
        #        tile_color = op_color(tile_color)
        #    tile_color = op_color(tile_color)
        #self.tiles = make_tiles_dict()
        self.turn = None
        self.castling_rights = None
        self.en_passant_rights = None
        self.halfmove_clock = None
        self.fullmove_clock = None
        pieces = self.fen_parse(self.fen_str)
        self.pieces_dict = self.make_pieces_dict(pieces)
        
        
        '''
        # parse given FEN and create board layout
        fields = fen.split()
        if not len(fields) == 6:
            raise ChessError('Invalid FEN given to board',
                             'Phantom.core.board.Board.__init__')
        pieces = fields[0]
        moving_color = fields[1]
        castling = fields[2]
        en_passant = fields[3]
        halfmove = int(fields[4])
        fullmove = int(fields[5])

        self.halfmove_clock = halfmove
        self.fullmove_clock = fullmove
        self.turn = 'white' if moving_color.lower() == 'w' else 'black'
        self.castling_rights = castling
        self.en_passant_rights = en_passant

        # parse the FEN into a board layout
        rank_split = '/'
        # 671: not used
        # is_rank_split = lambda char: char == rank_split
        is_file_split = lambda char: char in '12345678'
        is_white_chr = lambda char: char in 'RNBKQP'
        is_black_chr = lambda char: char in 'rnbkqp'
        is_piece_chr = lambda char: is_white_chr(char) or is_black_chr(char)

        ranks = pieces.split(rank_split)
        #print(ranks)
        y_c = C.grid_height
        for rank in ranks:
            y_c -= 1
            if y_c < 0:
                break
            fileind = 0
            for char in rank:
                if is_piece_chr(char):
                    klass = ChessPiece.type_from_chr(char)
                    #print(fileind, y_c)
                    pos = Coord(fileind, y_c)
                    #owner = self.player1 if is_white_chr(char) else self.player2
                    #color = owner.color
                    color = 'white' if is_white_chr(char) else 'black'
                    owner = self.get_player_by_color(color)
                    print(pos, color, owner)
                    newpiece = klass(pos, color, owner)
                    if newpiece.coord not in klass.default_origins:
                        # 671: this test isnt color-sensitive, could cause problems
                        newpiece.first_move = False
                    self.pieces.add(newpiece)
                elif is_file_split(char):
                    fileind += int(char)
                    continue
                fileind += 1
        '''

    def fen_parse(self, fen_str):
        # parse given FEN and create board layout
        fields = fen_str.split()
        if not len(fields) == 6:
            raise ChessError('Invalid FEN given to board',
                             'Phantom.core.board.fen_parse')
        pieces, moving_color, castling, en_passant, halfmove, fullmove = fields
        self.turn = 'white' if moving_color.lower() == 'w' else 'black'
        self.castling_rights = castling
        self.en_passant_rights = en_passant
        self.halfmove_clock = int(halfmove)
        self.fullmove_clock = int(fullmove)
        return pieces

    # Do players need to make / own their pieces?
    def make_piece(self, fen_loc, fen_char):
        fmt =  'Invalid fen_char: {} not in {}.'
        assert fen_char in C.fen_chars, fmt.format(fen_char, C.fen_chars)
        color = 'white' if fen_char in C.white_chars else 'black'
        return self.players_dict[color].make_piece(fen_loc, fen_char)

    def make_pieces_dict(self, pieces_fen):
        pieces_dict = _make_pieces_dict(pieces_fen)
        # replace each fen_char in the dict with a real Piece object
        for fen_loc, fen_char in pieces_dict.iteritems():
            pieces_dict[fen_loc] = self.make_piece(fen_loc, fen_char)
        return pieces_dict

    @property
    def players(self):
        return self.players_dict.itervalues()

    @property
    def tiles(self):
        return self.tiles_dict.itervalues()
    
    @property
    def pieces(self):
        return self.pieces_dict.itervalues()

    def __contains__(self, elem):
        return elem in self.pieces

    def __hash__(self):
        return int(self._uuid) % len(self.pieces) + self.fullmove_clock

    # implementation detail 0, 1
    def __getitem__(self, fen_loc):
        assert C.is_valid_fen_loc(fen_loc), '__getitem__({})'.format(fen_loc)
        return self.pieces_dict.get(fen_loc, None)
        #possible = []
        #for piece in self.pieces:
        #    if piece.coord == x:
        #        possible.append(piece)
        ## if there was only one item, return it otherwise a list of them all
        #if len(possible) == 0:
        #    return None
        #return possible[0] if len(possible) == 1 else possible

    def disp_char(self, fen_loc):
        if fen_loc in self.pieces_dict:
            return self.pieces_dict[fen_loc].disp_char
        else:
            return self.tiles_dict[fen_loc].disp_char

    def tile_at(self, pos):
        return self.tiles[pos.as_chess]
        #print('pos:', pos)
        #for tile in self.tiles:
        #    if tile.coord == pos:
        #        return tile
    
    def get_player_by_color(self, color):
        return self.player_dict[color]

    def get_piece_list(self, ptype=None, color=None):
        pieces = self.pieces
        pieces = [p for p in pieces if p.ptype == ptype] if ptype else pieces
        return   [p for p in pieces if p.color == color] if color else pieces

    @call_trace(4)
    def as_fen_str(self):
        rank_split = '/'
        fen = ''
        #for y in range(C.grid_height, -1, -1):
        for y in C.y_chars:
            file_gap = 0
            #for x in range(C.grid_width):
            for x in C.x_chars:
                fen_loc = x+y
                piece = self[fen_loc]
                if not piece:
                    file_gap += 1
                    continue
                else:
                    if file_gap > 0:
                        fen += str(file_gap)
                        file_gap = 0
                    fen += piece.fen_char
            #if y not in (8, 0):
            if y != '1':
                if file_gap > 0:
                    fen += str(file_gap)
                fen += rank_split
        self.upd_rights()  # make sure the castling rights aren't ''
        fen += ' {turn} {castle} {ep} {half} {full}'.format(
                turn=self.turn[0], castle=self.castling_rights,
                ep=self.en_passant_rights, half=self.halfmove_clock,
                full=self.fullmove_clock)
        print(fen)
        return fen

    def all_legal(self):
        ret = {}
        for piece in self.pieces:
            try:
                ret.update({piece: piece.valid()})
            except AttributeError:  # ccc: why would this exception be thrown?
                continue
        return ret

    def _pprnt(self):
        dash   = '–' if self.cfg.use_unicode else '-'
        turn_indicator = ' ' + C.turn_indicator[int(C.use_unicode)]  # zero or one
        header = '  ' + ' '.join(C.x_chars)
        lines = [self.name.center(19), dash * 19, header]
        fmt = '{} {} {}{}'
        for y in C.y_chars:
            pieces = ' '.join(self.disp_char(x+y) for x in C.x_chars)
            ti = turn_indicator if ((y == '1' and self.turn == 'white')
                                 or (y == '8' and self.turn == 'black')) else ''
            lines.append(fmt.format(y, pieces, y, ti))
        lines.append(header)
        return '\n'.join(lines).encode(C.default_encoding)          

    def _zpprnt(self):
        dash   = '–' if self.cfg.use_unicode else '-'
        turn_indicator = ' ' + C.turn_indicator[int(C.use_unicode)]  # zero or one
        lines = [self.name.center(19), dash * 19]
        for y in range(C.grid_height, -2, -1):
            line = []
            for x in range(-1, C.grid_width+1):
                if y in (-1, 8) and not (x in (-1, 8)):
                    char = Coord.tochesskeys[x+1]
                elif y in range(0, 8) and x in (-1, 8):
                    char = str(y+1)
                    if x == 8 and self.cfg.disp_turn:
                        if ((y == 0 and self.turn == 'white')
                         or (y == 7 and self.turn == 'black')):
                            char += turn_indicator
                elif x in (-1, 8):
                    char = ' '
                else:
                    piece = self[Coord(x, y)]
                    if piece:
                        char = piece.disp_char
                    else:
                        char = self.tile_at(Coord(x, y)).char if self.cfg.disp_sqrs else ' '
                line.append(char)
            lines.append(' '.join(line))
        return '\n'.join(lines).encode(C.default_encoding)

    def pprint(self):
        """Print a pretty version of the board."""
        if C.in_pythonista:
            import console
            console.set_font('DejaVuSansMono', 18)
            print(self._pprnt())
            console.set_font()
        else:
            print(self._pprnt())

    def __str__(self):
        return self.fen_str()

    def save(self, name):
        self.set_name(name)
        save(self)

    def set_name(self, name):
        self.name = name

    def set_game(self, g):
        self.game = g
        self.cfg.set_game(g)

    #freeze:def freeze(self):
    #freeze:    """Lock the board in place."""
    #freeze:    self.isfrozen = True
    #freeze:    #self.pieces = list(self.pieces)
    #freeze:    for player in self.players:
    #freeze:        player.freeze()

    #freeze:def unfreeze(self):
    #freeze:    """Unlock the board."""
    #freeze:    self.isfrozen = False
    #freeze:    #self.pieces = set(self.pieces)
    #freeze:    for player in self.players:
    #freeze:        player.unfreeze()

    #freeze:@contextlib.contextmanager
    #freeze:def frozen(self):
    #freeze:    self.freeze()
    #freeze:    yield
    #freeze:    self.unfreeze()

    def premove(self):
        """Freeze everything and send a signal to players that a move will be
        made."""
        #freeze:self.freeze()
        for player in self.players:
            player.premove()

    def postmove(self):
        """Unfreeze and send a signal to players that a move has been
        completed."""
        #freeze:self.unfreeze()
        #freeze:for player in self.players:
        #freeze:    player.postmove()

    def switch_turn(self):
        for player in self.players:
            if player.color == self.turn:
                player.timer.pause()
            else:
                player.timer.resume()
            self.turn = self.op_color(self.turn)

    def upd_rights(self):
        """This method soely exists so that if an exception occurs during a
        method that should have reset either en passant rights or castling
        rights and wasnt able to because of the error.  This method will find
        any '' strings and correct them to '-'."""
        self.castling_rights = self.castling_rights or '-'
        self.en_passant_rights = self.en_passant_rights or '-'

    #@call_trace(2)
    #@exc_catch(KeyError, ret='Could not kill specified piece', log=3)
    #def kill(self, piece):
    #    if not piece:
    #        return
    #    self.halfmove_clock = 0
    #    piece.owner.lose_piece(piece)
    #    self.dead.add(piece)
    #    self.pieces.remove(piece)

    # accepts: move('a1', 'b2') or move('a1b2')
    @call_trace(1)
    @exc_catch(LogicError, ChessError, KeyError,
               ret='Cannot make specified move', log=4)
    def move(self, srce, dest=None):
        if not dest:         # if srce == 'a1b2':
            dest = srce[2:]  #     dest = 'b2'
            srce = srce[:2]  #     srce = 'a1'
        print('bd move: {} --> {}'.format(srce, dest))
        assert C.is_valid_fen_loc(srce)
        assert C.is_valid_fen_loc(dest)
        #freeze:if self.isfrozen:
        #freeze:    raise LogicError('Board is frozen and cannot move',
        #freeze:                     'Phantom.core.board.Board.move()')
        piece = self[srce]
        if not piece:
            raise ChessError('No piece at {}'.format(srce),
                             'Phantom.core.board.Board.move()')
        target = self[dest]
        if target and target.owner == piece.owner:
            print('You can not kill one of your own men!')
            return False

        self.premove()
        player = piece.owner
        if not player.validatemove(srce, dest):
            print('Move in not valid and was rejected: {} --> {}'.format(srce, dest))
            return False
        print('True = {}.validatemove({}, {})'.format(player, srce, dest))
        if True:  # is_valid or self.cfg.force_moves:
            log_msg('move: specified move is valid, continuing', 3)
            # update castling rights
            if piece.ptype == 'rook':
                castling_partner = {'a1' : 'Q',
                                    'h1' : 'K',
                                    'a8' : 'q',
                                    'h8' : 'k'}.get(piece.fen_loc, '')
                self.castling_rights = self.castling_rights.replace(castling_partner, '')
            elif piece.ptype == 'king':  # ccc: if __queen__ moves, can she stll castle?
                if piece.color == 'white':
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                elif piece.color == 'black':
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')

            # update en_passant rights
            self.en_passant_rights = '-'  # ccc: FIXME
            #if piece.ptype == 'pawn':
            #    if piece.first_move:
            #        if round_down(dist(srce, dest)) == 2:
            #            file = piece.coord.as_chess[0]
            #            if piece.color == 'black':
            #                self.en_passant_rights = '{}6'.format(file)
            #            elif piece.color == 'white':
            #                self.en_passant_rights = '{}3'.format(file)

            # update halfmove & fullmove

            # Here we update the halfmove_clock BEFORE it is altered, to save
            # some else clauses later on.  We simply use a few ifs to determine
            # if it needs to be reset.
            self.halfmove_clock += 1

            if piece.ptype == 'pawn':
                self.halfmove_clock = 0
            if piece.color == 'black':
                self.fullmove_clock += 1

            #target = self[dest]
            #if self.data.get('move_en_passant', None):
            #    if piece.color == 'white':
            #        target = self[srce - Coord(0, 1)]
            #    elif piece.color == 'black':
            #        target = self[srce + Coord(0, 1)]
            #    self.data['move_en_passant'] = False

            #player.make_move(p1, p2)
            print(0, piece, srce, dest)
            print('sb', self.pieces_dict.get(srce, None))
            piece = self.pieces_dict.pop(srce)  # vacate srce square
            print('sa', self.pieces_dict.get(srce, None))
            print(1, piece.fen_loc)
            piece.fen_loc = dest
            print(2, piece.fen_loc)
            print('db', self.pieces_dict.get(dest, None))
            self.pieces_dict[dest] = piece      # links piece and unlinks target
            print('da', self.pieces_dict.get(dest, None))
            print(3, piece, srce, dest)

            #self.kill(target)
            self.lastmove = (srce, dest)
            self.switch_turn()
            self.postmove()
            print(4)
        else:
            assert False, 'if True: above!!'
            self.postmove()
            log_msg('move: specified move is invalid', 2, err=True)
            raise InvalidMove('Attempted move ({} -> {}) is invalid!'.format(
                              srce, dest), 'Phantom.core.board.Board.move()')
        #freeze:self.unfreeze()
        print('return True')
        return True

    def castle(self, pos):
        """Castle a king.
        :param str pos: must be in ('K', 'Q', 'k', 'q') - the side & color to
        castle on
        """
        if pos not in self.castling_rights:
            raise InvalidMove("Cannot castle {}".format(pos))
        if pos == pos.upper():
            # white
            if pos == 'K':
                if (self[Coord(5, 0)] is None) and (self[Coord(6, 0)] is None):
                    self.premove()
                    self[Coord(4, 0)].move(Coord(6, 0))
                    self[Coord(7, 0)].move(Coord(5, 0))
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                    self.postmove()
                    self.switch_turn()
                    return
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos),
                                      'Phantom.core.board.Board.castle()')
            elif pos == 'Q':
                if (self[Coord(3, 0)] is None) and (
                   self[Coord(2, 0)] is None) and (
                   self[Coord(1, 0)] is None):
                    self.premove()
                    self[Coord(4, 0)].move(Coord(2, 0))
                    self[Coord(0, 0)].move(Coord(3, 0))
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                    self.postmove()
                    self.switch_turn()
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos),
                                      'Phantom.core.board.Board.castle()')
        elif pos == pos.lower():
            if pos == 'k':
                if (self[Coord(5, 7)] is None) and (self[Coord(6, 7)] is None):
                    self.premove()
                    self[Coord(4, 7)].move(Coord(6, 7))
                    self[Coord(7, 7)].move(Coord(5, 7))
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')
                    self.postmove()
                    self.switch_turn()
                    return
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos),
                                      'Phantom.core.board.Board.castle()')
            elif pos == 'q':
                if (self[Coord(3, 7)] is None) and (
                   self[Coord(2, 7)] is None) and (
                   self[Coord(1, 7)] is None):
                    self.premove()
                    self[Coord(4, 7)].move(Coord(2, 7))
                    self[Coord(0, 7)].move(Coord(3, 7))
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')
                    self.postmove()
                    self.switch_turn()
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos),
                                      'Phantom.core.board.Board.castle()')
        if self.castling_rights == '':
            self.castling_rights = '-'

    @call_trace(3)
    @exc_catch(ChessError, LogicError, ret='Cannot promote', log=2)
    def promote(self, pos, to):
        if isinstance(pos, str):
            pos = Coord.from_chess(pos)
        elif isinstance(pos, Coord):
            pos = pos
        pawn = self[pos]
        if pawn.ptype != 'pawn':
            raise ChessError('Piece {} is not a pawn'.format(pawn), 'Phantom.core.board.Board.promote()')
        if to not in 'RNBQ':
            raise LogicError('Cannot promote pawn to piece type "{}"'.format(to), 'Phantom.core.board.Board.promote()')
        if pawn.color == 'black':
            if pawn.coord.y != 1:
                raise ChessError('Cannot promote {}'.format(pawn), 'Phantom.core.board.Board.promote()')
            x = pawn.coord.x
            newcls = ChessPiece.type_from_chr(to)
            color = pawn.color
            newpos = Coord(x, 0)
            new = newcls(newpos, color, pawn.owner)
            #freeze:self.freeze()
            self.pieces.append(new)
            #freeze:self.unfreeze()
            self.kill(pawn)
        elif pawn.color == 'white':
            if pawn.coord.y != 6:
                raise ChessError('Cannot promote {}'.format(pawn), 'Phantom.core.board.Board.promote()')
            x = pawn.coord.x
            newcls = ChessPiece.type_from_chr(to)
            color = pawn.color
            newpos = Coord(x, 7)
            new = newcls(newpos, color, pawn.owner)
            #freeze:self.freeze()
            self.pieces.append(new)
            #freeze:self.unfreeze()
            self.kill(pawn)
        self.switch_turn()

    def set_checkmate_validation(self, val):
        self.cfg.do_checkmate = val

    # TODO: make this work
    def is_checkmate(self):
        if not self.cfg.do_checkmate:
            return False
        return False

    # TODO: make this work
    def will_checkmate(self, p1, p2):
        if not self.cfg.do_checkmate:
            return False
        test = Board(fen=self.fen_str())
        test.move(p1, p2)
        test.cfg.do_checkmate = self.cfg.do_checkmate
        return test.is_checkmate()
__all__.append('Board')

if __name__ == '__main__':
    from Phantom.core.game_class import ChessGame
    b = Board(ChessGame())
    b.set_name('Chess')
    b.pprint()
