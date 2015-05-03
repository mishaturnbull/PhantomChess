# coding: utf-8

import os, sk
from Phantom.core.coord.point import Coord
import Phantom.constants as C

img_dir = '../gui_pythonista/imgs'

class Game (sk.Scene):
    def __init__(self, game):
        sk.Scene.__init__(self)
        self.game = game
        self.name = 'GameNode'
        chess_pieces_dict = self.create_pieces_sprite_dict()
        background_tile_dict = self.create_background_tiles_dict()
        for i, piece_name in enumerate(sorted(chess_pieces_dict)):
            node = chess_pieces_dict[piece_name]
            node.name = piece_name
            node.position += ((i+1) * 80, 20 + (i+1) * 50)
            node.alpha = 0.5
            self.add_child(node)
        for pos in background_tile_dict:
            self.add_child(background_tile_dict[pos])
        for piece in self.get_children_with_name('*'):
            print(piece.name, piece.frame)

        self.selected = None
        self.target_pos = None
        self.selected_pos = None


    @classmethod
    def create_pieces_sprite_dict(cls, piece_types=None):
        # returns a dict of {piece_short_name : piece_as_sk.SpriteNode} entries
        piece_types = piece_types or 'pawn rook queen king bishop knight'.split()
        short_names = ('{} {}'.format(color, type) for type in piece_types
                                                   for color in ('black', 'white'))
        fmt = os.path.join(img_dir, 'Chess set images {}.jpg')
        return {name:sk.SpriteNode(sk.Texture(fmt.format(name))) for name in short_names}

    @classmethod
    def create_background_tiles_dict(cls):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          colored_square_as_sk.Spritenode}
        # useful for node hit-testing,much simplifies touch_began
        ret = {}
        size = sk.Size(C.scale_factor, C.scale_factor)
        for tile in self.game.board.tiles:
            node = sk.SpriteNode()
            node.size = size
            node.alpha = 0.3
            node.position = tile.coord.as_screen()
            node.color = tile.tilecolor
            ret.update({tile.coord: node})
        return ret

    def did_change_size(self, old_size):
        pass

    def update(self):
        pass

    def touch_began(self, node, touch):
        pass

    def touch_moved(self, node, touch):
        pass

    def touch_ended(self, node, touch):
        pass

def main():
    print('=' * 30)
    game = Game()
    scene_view = sk.View(game)
    scene_view.shows_fps = True
    scene_view.present()

if __name__ == '__main__':
    main()
