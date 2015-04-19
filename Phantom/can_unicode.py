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
(successful) use of unicode characters and defaults to a monospaced font."""

import platform

# The default terminal on Windows currently has two problems:
# 1) It does not support Unicode!
# 2) It can not be configured to default to a monospaced font

unicode_systems_dict = {
    'Darwin'  : True,    # Mac OSX and Pythonista for iOS
    'Java'    : True,    # Jython
    'Linux'   : True,    # Works like Darwin
    'Windows' : False }  # Lacks Unicode support

def can_unicode():
    return unicode_systems_dict.get(platform.system(), False)

if __name__ == '__main__':
    print('can_unicode(): {}'.format(can_unicode()))
