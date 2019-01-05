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
            self.pr_roll.width *= 1.1
            self.pr_roll.draw_noteoverlay()
            self.pr_roll.draw_canvas()            
            #print('zoom out', self.pr_roll.width)

        # zoom in
        elif text == 'h':
            self.pr_roll.width *= 0.9
            self.pr_roll.draw_noteoverlay()
            self.pr_roll.draw_canvas()
            #print('zoom in', self.pr_roll.width)

        return True


