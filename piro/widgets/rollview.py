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

        # viewport based on roll size
        self.local_left = None
        self.local_right = None

        # members
        self.pr_roll = PrRoll()

        # binds
        self.bind(scroll_x=self.update)
        self.bind(size=self.update)

        # child layout
        self.add_widget(self.pr_roll)

    # bind callbacks
    def update(self, instance=None, scroll_x=None):
        self.local_left = self.to_local(self.x, 0)[0]
        self.local_right = self.to_local(self.width + self.x, 0)[0]

    # zoom in/out
    def zoom_in(self):
        self.pr_roll.zoom_in()
        self.update()
    def zoom_out(self):
        self.pr_roll.zoom_out()
        self.update()
    def zoom_to(self, factor):
        self.pr_rooll.zoom_to(factor)
        self.update()
    

