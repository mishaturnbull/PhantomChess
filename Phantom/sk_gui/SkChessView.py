#!/usr/bin/env python
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

from __future__ import (absolute_import, division, print_function, unicode_literals)

import dialogs, photos, sk, sys, ui
#import SkChessBoardScene ; reload(SkChessBoardScene)  #Pythonista workaround
from Phantom.sk_gui.SkChessBoardScene import SkChessBoardScene
from Phantom.core.game_class import ChessGame

def quit_action(sender):
    msg = '{} is not yet implemented!!'.format(sender.title)
    dialogs.hud_alert(msg)
    print(msg)
    #sys.exit(msg)

def center_square():
    w, h = ui.get_screen_size()
    if w > h:  # landscape
        return ((w - h) / 2, 0, h, h)
    else:  # portrait
        return (0, (h - w) / 2, w, w)

class SkChessView(ui.View):
    def __init__(self, game=None):
        self.width, self.height = ui.get_screen_size()
        if photos.is_authorized():
            self.add_subview(self.make_image_view())
        game = game or ChessGame()
        board_scene = self.make_board_scene(game)
        self.make_buttons()
        self.present(orientations=['landscape'], hide_title_bar=True)

    def make_image_view(self, image_name=''):
        image_view = ui.ImageView(frame=self.bounds)
        image_view.image = ui.Image.from_data(photos.get_image(raw_data=True)) # ui.Image('emj:Smiling_1')
        return image_view

    def make_board_scene(self, game):
        board_scene = SkChessBoardScene(game)
        scene_view = sk.View(board_scene)
        scene_view.frame = center_square()
        # print(ui.get_screen_size(), scene_view.frame)
        scene_view.shows_fps = True
        scene_view.shows_node_count = True
        scene_view.shows_physics = True
        self.add_subview(scene_view)
        # scene_view.present()
        return board_scene

    @classmethod
    def make_button(cls, title, i):
        button = ui.Button(title=title)
        button.action = quit_action
        button.x = 30
        button.y = 105 * (i + 1)
        return button

    def make_buttons(self, menu_titles=None):
        menu_titles = menu_titles or 'Options AI_Easy AI_Hard Get_score Undo Deselect'.split()
        for i, title in enumerate(menu_titles):
            self.add_subview(self.make_button(title.replace('_', ' '), i))


def gui_sk(game=None):
    game = game or ChessGame()
    SkChessView(game)
    ## GameView(GameScene(game))  # throws TypeError
    # scene_view = sk.View(GameScene(game))
    # scene_view.shows_fps = True
    # scene_view.present()

if __name__ == '__main__':
    print('=' * 30)
    gui_sk()
