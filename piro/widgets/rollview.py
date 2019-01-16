from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
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

        # child layout
        self.add_widget(self.pr_roll)

    @property
    def local_left(self):
        return self.to_local(self.x, 0)[0]
    @property
    def local_right(self):
        return self.to_local(self.width + self.x, 0)[0]
    @property
    def scroll_width(self):
        return self.pr_roll.width - self.width

    # bind callbacks
    def update(self, instance=None):
        """Update local_left/right, scroll_width

        [Used by]
            PrRoll
                .focus
                .zoom_in
                .zoom_out
                .zoom_to

            PrRoot
                .draw_roll
                ._scroll_stop
                ._keydown - g/h/w/play/c
        """
        self.show()

    # show local left/right
    def show(self):        
        # print('local left/right/width/bar_x : '
        #     ,self.local_left, '/', self.local_right, '/'
        #     ,self.pr_roll.width, '/', self.parent.parent.bar_x)
        pass

    # focus
    def focus(self, x):
        """Scroll to the x"""
        if self.local_left <= x and x <= self.local_right:
            pass
        else:
            self.scroll_x = x / self.scroll_width          
            self.update_from_scroll()

    # zoom in/out
    def zoom_in(self):
        self.pr_roll.zoom_in()
    def zoom_out(self):
        self.pr_roll.zoom_out()
    def zoom_to(self, factor):
        self.pr_rooll.zoom_to(factor)

