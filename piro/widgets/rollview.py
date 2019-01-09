from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from piro.widgets.roll import PrRoll

class PrRollView(ScrollView):
    """Roll ScrollView, Accepts Key Up/Dn"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRollView, self).__init__(**kwargs)

        # props
        self.bar_width = 25
        self.scroll_type = ['bars']

        # members
        self.pr_roll = PrRoll()

        # binds
        Window.bind(on_key_up=self._keyup)
        Window.bind(on_key_down=self._keydown)

        # child layout
        self.add_widget(self.pr_roll)

    # bind callbacks
    def _keyup(self, *args):        
        return True

    def _keydown(self, instance, key, keycode, text, modifiers):

        # zoom out
        if text == 'g':
            self.pr_roll.zoom_in()
            print('zoom out', self.width, self.pr_roll.width, self.pr_roll.scale.x)

        # zoom in
        elif text == 'h':
            self.pr_roll.zoom_out()
            print('zoom in', self.width, self.pr_roll.width, self.pr_roll.scale.x)

        return True


