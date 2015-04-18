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

"""Deterime which platform you are using, and decide whether it supports
(successful) use of unicode characters."""

import platform


UNICODE_PLATFORMS = ('pythonista', 'osx')
KNOWN_OS = {'windows': lambda s: 'Windows' in s,
            'pythonista': lambda s: ('iPhone' in s) or ('iPad' in s),
            'osx': lambda s: 'Darwin' in s and not ('iPhone' in s) or
                   ('iPad' in s)
           }
DO_UNICODE = False  # assume false, enable if known to be allowed

USER_PLATFORM = platform.platform().lower()

def get_os(user_os):
    for os in KNOWN_OS:
        if KNOWN_OS[os](user_os):
            return os

def can_unicode(user_os):
    return user_os in UNICODE_PLATFORMS

DO_UNICODE = can_unicode(get_os(platform.platform()))
