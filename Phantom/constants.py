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

from Phantom.__version__ import __version__ as version
from Phantom.can_print_unicode import can_print_unicode
import sys

import ConfigParser as cfgparse
cfg_file_name = 'PhantomConfig.cfg'
cfg = cfgparse.ConfigParser()
cfg.read(cfg_file_name)

try:
    import ui
    in_pythonista = True
    screen_width, screen_height = ui.get_screen_size()
    del ui
except ImportError:
    in_pythonista = False
    screen_width = cfg.getint('general', 'screen_width')
    screen_height = cfg.getint('general', 'screen_height')

debug = cfg.getint('debug', 'level')

# if debug > exc_catch_cutoff, the exc_catch decorator does nothing
exc_catch_cutoff = cfg.getint('debug', 'exc_catch_cutoff')

# Use the unicode prettyprinter or an ASCII prettyprinter
# By default this is set to "in_pythonista", so that in the app unicode will
# be used but otherwise ASCII will be used.
# CCC: Turning use_unicode on by default
# 671: decide whether to use_unicode in `Phantom.can_print_unicode`
default_encoding = (sys.stdout.encoding or
                    ('cp437' if sys.platform.startswith('win') else 'utf-8'))

unicode_pref = cfg.get('general', 'use_unicode')
if unicode_pref == 'auto':
    use_unicode = can_print_unicode()
elif unicode_pref == 'true':
    use_unicode = True
else:
    use_unicode = False

grid_width = cfg.getint('internal', 'grid_width')
grid_height = cfg.getint('internal', 'grid_height')
grid_colors = eval(cfg.get('internal', 'grid_colors'))
scale_factor = cfg.getint('internal', 'scale_factor')

holder_point = eval(cfg.get('internal', 'holder_point'))

save_fen = cfg.get('internal', 'save_fen')
save_epd = cfg.get('internal', 'save_epd')
test_suite = cfg.get('internal', 'test_suite')
dbg_name  = cfg.get('internal', 'dbg_name')

piece_chars = {    # (as_ascii, as_unicode) or [int(use_unicode)]
    'white king'   : eval(cfg.get('piece_chars', 'white_king')),
    'white queen'  : eval(cfg.get('piece_chars', 'white_queen')),
    'white rook'   : eval(cfg.get('piece_chars', 'white_rook')),
    'white bishop' : eval(cfg.get('piece_chars', 'white_bishop')),
    'white knight' : eval(cfg.get('piece_chars', 'white_knight')),
    'white pawn'   : eval(cfg.get('piece_chars', 'white_pawn')),
    'black king'   : eval(cfg.get('piece_chars', 'black_king')),
    'black queen'  : eval(cfg.get('piece_chars', 'black_queen')),
    'black rook'   : eval(cfg.get('piece_chars', 'black_rook')),
    'black bishop' : eval(cfg.get('piece_chars', 'black_bishop')),
    'black knight' : eval(cfg.get('piece_chars', 'black_knight')),
    'black pawn'   : eval(cfg.get('piece_chars', 'black_pawn'))}

turn_indicator   = eval(cfg.get('piece_chars', 'turn_indicator'))
black_space_char = eval(cfg.get('piece_chars', 'black_space_char'))
white_space_char = eval(cfg.get('piece_chars', 'white_space_char'))



fen_rank_split = cfg.get('piece_chars', 'fen_rank_split')
default_halfmove = cfg.getint('piece_chars', 'default_halfmove')
default_fullmove = cfg.getint('piece_chars', 'default_fullmove')
start_turn = cfg.get('piece_chars', 'start_turn')
default_castle = cfg.get('piece_chars', 'default_castle')
default_ep = cfg.get('piece_chars', 'default_ep')

# use a formatted version to allow easier changes to settings
# (not that any changes are planned)
opening_fen = ('{r}{n}{b}{q}{k}{b}{n}{r}{S}'
               '{p}{p}{p}{p}{p}{p}{p}{p}{S}'
               '8{S}'
               '8{S}'
               '8{S}'
               '8{S}'
               '{P}{P}{P}{P}{P}{P}{P}{P}{S}'
               '{R}{N}{B}{Q}{K}{B}{N}{R}'
               ' {t} {c} {e} {h} {f}').format(r=piece_chars['black rook'][0],
                                              n=piece_chars['black knight'][0],
                                              b=piece_chars['black bishop'][0],
                                              q=piece_chars['black queen'][0],
                                              k=piece_chars['black king'][0],
                                              p=piece_chars['black pawn'][0],
                                              S=fen_rank_split,
                                              R=piece_chars['white rook'][0],
                                              N=piece_chars['white knight'][0],
                                              B=piece_chars['white bishop'][0],
                                              Q=piece_chars['white queen'][0],
                                              K=piece_chars['white king'][0],
                                              P=piece_chars['white pawn'][0],
                                              h=str(default_halfmove),
                                              f=str(default_fullmove),
                                              t=start_turn,
                                              c=default_castle,
                                              e=default_ep)

import os as _os
phantom_dir = _os.path.dirname(_os.path.realpath(__file__))
del _os

if in_pythonista:
    import scene
    screen_size = scene.Rect(0, 0, screen_width, screen_height)
    del scene
else:
    # if no Rect class is available, make a (much) simpler version with the
    # necessary attributes
    class Rect (object):
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
    screen_size = Rect(0, 0, screen_width, screen_height)


