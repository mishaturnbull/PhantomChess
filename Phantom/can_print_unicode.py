# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
import os, sys

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

"""Deterime your platform supports printing of unicode characters."""

fmt = '''
    PYTHONIOENCODING:    {}
    sys.stdout.encoding: {}
    sys.stderr.encoding: {}'''

def can_print_unicode(s='Welcome to PhantomChess...'):
    # python -c "import sys ; print(sys.stderr.encoding)"
    # 671's Windows box defaults to cp437 but a buddy in Germany's box defaults to cp850
    print('Before: ' + fmt.format(os.getenv('PYTHONIOENCODING', None),
                                 sys.stdout.encoding,
                                 sys.stderr.encoding))
    default_encoding = (sys.stdout.encoding
                        or ('cp437' if sys.platform.startswith('win') else 'utf-8'))
    if not os.getenv('PYTHONIOENCODING', None):  # PyInstaller workaround
        os.environ['PYTHONIOENCODING'] = default_encoding
    try:
        print(u'♜ ♞ ♝  {} ♗ ♘ ♖ '.format(s).encode(default_encoding))
        print('After: ' + fmt.format(os.getenv('PYTHONIOENCODING', None),
                                     sys.stdout.encoding,
                                     sys.stderr.encoding))
        return (sys.stdout.encoding == default_encoding.upper())  # True  # FIXME
    except UnicodeEncodeError:
        print(str(s))
        return False

if __name__ == '__main__':
    print(can_print_unicode())