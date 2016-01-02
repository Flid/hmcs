from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scrollview import ScrollView


class ScaleScrollView(ScatterLayout):
    def on_touch_move(self, touch):
        if touch.ud:
            touch.ud.pop('start_ind', None)
        return super(ScaleScrollView, self).on_touch_move(touch)

    def on_pos(self, instance, pos):
        if pos[0] >= 0:
            self.x = 0
        elif self.right < self.parent.width and self.width >= self.parent.width:
            self.right = self.parent.width

        if pos[1] >= 0:
            self.y = 0
        elif self.top < self.parent.height and self.height >= self.parent.height:
            self.top = self.parent.height
