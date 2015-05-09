#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sk, sys, ui
import SkChessBoardScene ; reload(SkChessBoardScene)  #Pythonista workaround
from SkChessBoardScene import SkChessBoardScene
from Phantom.core.game_class import ChessGame

def quit_action(sender):
    msg = '{} not implemented!!'.format(sender.title)
    print(msg)
    sys.exit(msg)

def center_square():
    w, h = ui.get_screen_size()
    if w > h:  # landscape
        return ((w - h) / 2, 0, h, h)
    else:  # portrait
        return (0, (h - w) / 2, w, w)

class SkChessView(ui.View):
    def __init__(self, game=None):
        game = game or ChessGame()
        board_scene = self.make_board_scene(game)
        self.make_buttons()
        self.present(orientations=['landscape'], hide_title_bar=True)

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
