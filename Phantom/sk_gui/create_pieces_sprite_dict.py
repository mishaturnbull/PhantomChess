# coding: utf-8

import os, sk

img_dir = '../gui_pythonista/imgs'

class Game (sk.Scene):
    def __init__(self):
        sk.Scene.__init__(self)
        self.name = 'GameNode'
        chess_pieces_dict = self.create_pieces_sprite_dict()
        for i, piece_name in enumerate(sorted(chess_pieces_dict)):
            node = chess_pieces_dict[piece_name]
            node.name = piece_name
            node.position += ((i+1) * 80, 20 + (i+1) * 50)
            self.add_child(node)
        for piece in self.get_children_with_name('*'):
            print(piece.name, piece.frame)

    @classmethod
    def create_pieces_sprite_dict(self, piece_types=None):
        # returns a dict of {piece_short_name : piece_as_sk.SpriteNode} entries
        piece_types = piece_types or 'pawn rook queen king bishop knight'.split()
        short_names = ('{} {}'.format(color, type) for type in piece_types
                                                   for color in ('black', 'white'))
        fmt = os.path.join(img_dir, 'Chess set images {}.jpg')
        return {name:sk.SpriteNode(sk.Texture(fmt.format(name))) for name in short_names}
        
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
