from math import sqrt, floor

from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image

HEX_HEIGHT = 100
HEX_WIDTH = HEX_HEIGHT / sqrt(3) * 2

SQRT3 = sqrt(3)

class EmptyHexagon(Image):
    pass


class GameBoard(FloatLayout):
    def __init__(self,*args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.tiles = []
        Clock.schedule_once(self.render_hexagons)

    def on_touch_down(self, touch):
        ix, iy = self.coords_to_ind(touch.x, touch.y)
        x, y = self.index_to_coord(ix, iy)

        self.main_h.pos = [
            x + self.center_x - HEX_WIDTH/2,
            y + self.center_y - HEX_HEIGHT/2,
        ]

    def on_touch_move(self, touch):
        self.on_touch_down(touch)

    def index_to_coord(self, ix, iy):
        x = HEX_WIDTH * ix * 3 / 4
        y = HEX_HEIGHT * (iy + ix / 2)
        return x, y

    def coords_to_ind(self, x, y):
        # TODO: optimize
        x = x - self.center_x + HEX_HEIGHT/sqrt(3)
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

    def render_hexagons(self, instance):
        def _add(ix, iy):
            x, y = self.index_to_coord(ix, iy)

            from random import random

            h = EmptyHexagon(
                pos=[
                    x + self.center_x - HEX_WIDTH/2,
                    y + self.center_y - HEX_HEIGHT/2,
                ],
                opacity=random(),
            )
            h.ind = (x, y)
            self.add_widget(h)

        BOARD_SIZE = 8
        for x in range(-BOARD_SIZE, BOARD_SIZE+1):
            for y in range(-BOARD_SIZE, BOARD_SIZE+1):
                if abs(x + y) > BOARD_SIZE:
                    continue
                _add(x, y)

        self.main_h = EmptyHexagon(
            pos=[0, 0],
            opacity=1,
        )
        self.add_widget(self.main_h)