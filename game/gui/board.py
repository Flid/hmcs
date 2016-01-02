from math import sqrt, floor

from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from .scale_scroll_view import ScaleScrollView
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.core.window import Window

SQRT3 = sqrt(3)

class EmptyHexagon(Image):
    pass


class UndiscoveredHexagon(Image):
    pass


class ScrollScaleLayout(ScrollView):
    pass


def pos_to_parent_chained(instance, target_parent):
    """
    Get `pos` of `instance` in target parent's coordinates.
    """
    pos = instance.to_parent(*instance.pos)

    while instance.parent != target_parent:
        instance = instance.parent
        pos = instance.to_parent(*pos)

    return pos


def pos_to_local(pos, current_layout, target_child):
    """
    Get `pos` of `instance` in target child`s coordinates.
    """
    parents = []

    child = target_child
    while child != current_layout:
        parents.append(child)
        child = child.parent

    while parents:
        parent = parents.pop()
        pos = parent.to_local(*pos)

    return pos


class BoardTopLayer(RelativeLayout):
    is_locked = BooleanProperty(False)
    current_tile = ObjectProperty(None)
    board = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(BoardTopLayer, self).__init__(*args, **kwargs)
        self.show_anim = Animation(opacity=1, duration=0.2)
        self.hide_anim = Animation(opacity=0, duration=0.2)

    def on_touch_down(self, touch):
        if not self.is_locked:
            return False

        if self.collide_point(*touch.pos):
            touch.grab(self, exclusive=True)
            return True

        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.collide_point(*touch.pos):
                self.hide_tile()
                return True

    def on_is_locked(self, instance, blocked):
        self.show_anim.stop(self)
        self.hide_anim.stop(self)

        if blocked:
            self.show_anim.start(self)
        else:
            self.hide_anim.start(self)

    def hide_tile(self):
        if self.current_tile is None:
            return

        self.is_locked = False
        self.remove_widget(self.current_tile)
        self._return_func(self.current_tile)

    def show_tile(self, tile, return_func):
        self._return_func = return_func
        self.current_tile = tile
        self.is_locked = True
        self.add_widget(tile)

        new_size = self.width * 0.75, self.height * 0.75
        new_pos = self.to_local(
            self.center_x - new_size[0] / 2,
            self.center_y - new_size[1] / 2,
        )
        tile.anim = Animation(
            x=new_pos[0],
            y=new_pos[0],
            width=new_size[0],
            height=new_size[1],
            transition='in_out_elastic',
        )
        tile.anim.start(tile)


class GameBoard(RelativeLayout):
    texture = ObjectProperty(None)
    main_ingame_screen = ObjectProperty(None)

    def __init__(self,*args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        self.board_size = 0
        self.tiles = {}
        self.tile_height = Window.dpi * 2
        self.tile_width = self.tile_height / SQRT3 * 2

    def on_size(self, instance, value):
        if not self.main_ingame_screen:
            return

        scale_min = self.main_ingame_screen.ids['game_area'].width / self.width
        scale_min = max(
            scale_min,
            self.main_ingame_screen.ids['game_area'].height / self.height,
        )

        if scale_min < 0.1:
            scale_min = 0.1
        elif scale_min > 1:
            scale_min = 1

        self.main_ingame_screen.ids['scroll_view'].scale_min = scale_min

    def on_touch_down(self, touch):
        res = self.coords_to_ind(touch.x, touch.y)
        if not res:
            return

        touch.grab(self)
        touch.ud = {'start_ind': res}

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return

        touch.ungrab(self)
        res = self.coords_to_ind(touch.x, touch.y)
        if res is None:
            return

        if touch.ud and touch.ud.get('start_ind') == res:
            tile = self.tiles[res]
            self.send_tile_to_top_layer(tile)
            return True

    def send_tile_to_top_layer(self, tile):
        new_pos = pos_to_parent_chained(tile, self.main_ingame_screen.ids['game_area'])
        self.remove_widget(tile)
        tile.pos = new_pos
        self.top_layer.show_tile(tile, self.return_tile_from_top_layer)

    def return_tile_from_top_layer(self, tile):
        tile.pos = pos_to_local(tile.pos, self.main_ingame_screen.ids['game_area'], self)
        self.add_widget(tile)

        target_pos = self.to_local(*self.index_to_coord(*tile.ind))
        target_pos = (
            target_pos[0] + self.center_x - self.tile_width / 2,
            target_pos[1] + self.center_y - self.tile_height / 2,
        )

        tile.anim = Animation(
            x=target_pos[0],
            y=target_pos[1],
            width=self.tile_width,
            height=self.tile_height,
            transition='in_out_elastic',
        )
        tile.anim.start(tile)

    def on_touch_move(self, touch):
        res = self.coords_to_ind(touch.x, touch.y)
        if not res:
            return

        ix, iy = res
        x, y = self.index_to_coord(ix, iy)

        self.hover_hex.pos = [
            x + self.center_x - self.x - self.tile_width / 2,
            y + self.center_y - self.y - self.tile_height / 2,
        ]

    def index_to_coord(self, ix, iy):
        x = self.tile_width * ix * 3 / 4.0
        y = self.tile_height * (iy + ix / 2.0)
        return x, y

    def coords_to_ind(self, x, y):
        # TODO: optimize
        x = x - self.center_x + self.tile_height/SQRT3
        y = y - self.center_y + self.tile_height/2

        block_width = self.tile_height * SQRT3 / 2
        block_height = self.tile_height

        block_x = floor(x / block_width)
        block_y = floor(y / block_height)

        dx = x - block_x * block_width
        dy = y - block_y * block_height

        x_shift = 0
        y_shift = 0

        if block_x % 2 == 0:
            if dy < (self.tile_height / 2 - dx * SQRT3):
                x_shift = -1
            elif dy > block_height - (self.tile_height / 2 - dx * SQRT3):
                x_shift = -1
                y_shift = 1
        else:
            if dy < min(dx*SQRT3, self.tile_height/2):
                y_shift = -0.5
            elif dy > max(self.tile_height - dx*SQRT3, self.tile_height/2):
                y_shift = 0.5
            else:
                x_shift = -1
                y_shift = 0.5

        ix = block_x + x_shift
        iy = round(block_y - block_x / 2 + y_shift)

        if abs(ix + iy) > self.board_size or max(abs(ix), abs(iy)) > self.board_size:
            return

        return ix, iy

    def clear_board(self):
        for tile in self.tiles.values():
            self.remove_widget(tile)

    def render_hexagons(self, size):
        self.board_size = size
        self.clear_board()
        self.width = (size * 2 + 3) * self.tile_width * 3 / 4.0
        self.height = (size * 2 + 3) * self.tile_height
        self.parent.size = self.size
        self.parent.parent.size = self.size

        def _add(ix, iy):
            x, y = self.index_to_coord(ix, iy)

            h = UndiscoveredHexagon(
                pos=[
                    x + self.center_x - self.x - self.tile_width / 2,
                    y + self.center_y - self.y - self.tile_height / 2,
                ],
            )
            h.size = (self.tile_width, self.tile_height)
            h.ind = (ix, iy)
            self.tiles[h.ind] = h
            self.add_widget(h)

        for x in range(-size, size + 1):
            for y in range(-size, size + 1):
                if abs(x + y) > size:
                    continue
                _add(x, y)

        self.texture = Image(source='static/background.jpg').texture
        self.texture.wrap = 'repeat'

        self.remove_widget(self.hover_hex)
        self.add_widget(self.hover_hex)
