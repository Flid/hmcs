from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scrollview import ScrollView


class ScaleScrollView(ScatterLayout):

    def on_touch_move(self, touch):
        if touch.ud:
            touch.ud.pop('start_ind', None)
        super(ScaleScrollView, self).on_touch_move(touch)