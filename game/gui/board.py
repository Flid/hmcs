from math import sqrt, floor

from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.image import Image

SQRT3 = sqrt(3)
HEX_HEIGHT = 100
HEX_WIDTH = HEX_HEIGHT / SQRT3 * 2


class EmptyHexagon(Image):
    pass


class GameBoard(RelativeLayout):
    texture = ObjectProperty(None)

    def __init__(self,*args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.tiles = {}

    def on_touch_down(self, touch):
        ix, iy = self.coords_to_ind(touch.x, touch.y)
        x, y = self.index_to_coord(ix, iy)

        self.hover_hex.pos = [
            x + self.center_x - self.x - HEX_WIDTH/2,
            y + self.center_y - self.y - HEX_HEIGHT/2,
        ]

    def on_touch_move(self, touch):
        self.on_touch_down(touch)

    def index_to_coord(self, ix, iy):
        x = HEX_WIDTH * ix * 3 / 4
        y = HEX_HEIGHT * (iy + ix / 2)
        return x, y

    def coords_to_ind(self, x, y):
        # TODO: optimize
        x = x - self.center_x + HEX_HEIGHT/SQRT3
        y = y - self.center_y + HEX_HEIGHT/2

        block_width = HEX_HEIGHT * SQRT3 / 2
        block_height = HEX_HEIGHT

        block_x = floor(x / block_width)
        block_y = floor(y / block_height)

        dx = x - block_x * block_width
        dy = y - block_y * block_height

        x_shift = 0
        y_shift = 0

        if block_x % 2 == 0:
            if dy < (HEX_HEIGHT / 2 - dx * SQRT3):
                x_shift = -1
            elif dy > block_height - (HEX_HEIGHT / 2 - dx * SQRT3):
                x_shift = -1
                y_shift = 1
        else:
            if dy < min(dx*SQRT3, HEX_HEIGHT/2):
                y_shift = -0.5
            elif dy > max(HEX_HEIGHT - dx*SQRT3, HEX_HEIGHT/2):
                y_shift = 0.5
            else:
                x_shift = -1
                y_shift = 0.5

        ix = block_x + x_shift
        iy = round(block_y - block_x / 2 + y_shift)

        return ix, iy

    def clear_board(self):
        for tile in self.tiles.values():
            self.remove_widget(tile)

    def render_hexagons(self, size):
        self.clear_board()

        def _add(ix, iy):
            x, y = self.index_to_coord(ix, iy)

            h = EmptyHexagon(
                pos=[
                    x + self.center_x - self.x - HEX_WIDTH/2,
                    y + self.center_y - self.y - HEX_HEIGHT/2,
                ],
            )
            h.ind = (x, y)
            self.tiles[h.ind] = h
            self.add_widget(h)

        for x in range(-size, size+1):
            for y in range(-size, size+1):
                if abs(x + y) > size:
                    continue
                _add(x, y)


        self.texture = Image(source='static/background.jpg').texture
        self.texture.wrap = 'repeat'
