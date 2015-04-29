#!/usr/bin/env python
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

"""The main scene object for the GUI.  Allows use of multiple scene classes with one GUI."""

try:
    import scene
    try:
        from Phantom.core.chessobj import PhantomObj
        from Phantom.boardio.boardcfg import Namespace
        from Phantom.gui_pythonista.screen_main import ChessMainScreen
        from Phantom.gui_pythonista.screen_loading import ChessLoadingScreen
        #from Phantom.gui_pythonista.screen_options import ChessOptionsScreen
        #from Phantom.gui_pythonista.screen_promote import ChessPromoteScreen
    except ImportError as e:
        print(e)
        raise e
except ImportError:
    pass

class MultiScene (scene.Scene, PhantomObj):
    
    def __init__(self, start_scene):
        self.active_scene = start_scene
        self.tmp_t = 0
        self.invocations = 0
        #self.data = Namespace()
        self.scenes = {key : None for key in
                        'debug load main options promote'.split()}
        #self.scenes['load'] = start_scene
        self.set_load_scene(start_scene)

    def switch_scene(self, new_scene):
        assert new_scene
        new_scene.bounds = self.bounds
        new_scene.setup()
        self.active_scene = new_scene

    def setup(self):
        self.active_scene = self.scenes['load']
        self.tmp_t = self.t
        self.active_scene.bounds = self.bounds
        self.active_scene.setup()

    def draw(self):
        self.invocations += 1
        scene.background(0, 0, 0)
        scene.fill(1, 0, 0)
        self.active_scene.touches = self.touches
        self.active_scene.t = self.t - self.tmp_t
        self.active_scene.draw()

    def touch_began(self, touch):
        self.active_scene.touch_began(touch)
        
    def touch_moved(self, touch):
        self.active_scene.touch_moved(touch)
        
    def touch_ended(self, touch):
        self.active_scene.touch_ended(touch)
    
    def set_main_scene(self, s):
        self.scenes['main'] = s
        #self.main_scene = s
    
    def set_load_scene(self, s):
        self.scenes['load'] = s
        #self.load_scene = s
    
    def set_dbg_scene(self, s):
        self.scenes['debug'] = s
        #self.dbg_scene = s
    
    def set_options_scene(self, s):
        self.scenes['options'] = s
        #self.options_scene = s
    
    def set_promote_scene(self, s):
        self.scenes['promote'] = s
        #self.promote_scene = s
    
    def did_begin(self):
        #self.switch_scene(self.main_scene)
        self.switch_scene(self)  #self.scenes['main'])

    def run_gui(self, game):
        #from Phantom.gui_pythonista.main_scene import MultiScene
        #multi_scene = MultiScene(ChessLoadingScreen())
        #self.data['screen_main'] = ChessMainScreen(game, self)
        #self.data['screen_load'] = ChessLoadingScreen()
        #zself.data['screen_options'] = ChessOptionsScreen(game, self)
        #zself.data['screen_promote'] = ChessPromoteScreen(game, self)
        #zself.data['main_scene'] = MultiScene(ChessLoadingScreen())
        ##self.data['screen_main'].set_parent(self.data['main_scene'])
        #self.data['screen_load'].parent = self.data['main_scene']
        ##self.data['screen_options'].set_parent(self.data['main_scene'])
        ##self.data['screen_promote'].set_parent(self.data['main_scene'])
        #self.data['main_scene'].switch_scene(self.data['screen_load'])
        self.scenes['main'] = ChessMainScreen(game, self)
        self.scenes['options'] = ChessOptionsScreen(game, self)
        self.scenes['promote'] = ChessPromoteScreen(game, self)
        scene.run(self, orientation=scene.LANDSCAPE)

if __name__ == '__main__':
    from Phantom.core.game_class import ChessGame
    game = ChessGame()
    game.gui()
