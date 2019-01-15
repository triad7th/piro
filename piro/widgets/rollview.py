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

        # viewport based on roll size
        self.local_left = None
        self.local_right = None
        self.scroll_width = None

        # members
        self.pr_roll = PrRoll()

        # child layout
        self.add_widget(self.pr_roll)

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
        self.local_left = self.to_local(self.x, 0)[0]
        self.local_right = self.to_local(self.width + self.x, 0)[0]
        self.scroll_width = self.pr_roll.width - self.width
        self.show()

    # show local left/right
    def show(self):
        print('local left/right/width/bar_x : '
            ,self.local_left, '/', self.local_right, '/'
            ,self.pr_roll.width, '/', self.parent.parent.bar_x)

    # focus
    def focus(self, x):
        """Scroll to the x"""
        if self.local_left <= x and x <= self.local_right:
            pass
        else:
            self.scroll_x = x / self.scroll_width          
            self.update_from_scroll()
            self.update()

    # zoom in/out
    def zoom_in(self):
        print('zoom in!')
        self.pr_roll.zoom_in()
        Clock.schedule_once(self.update, 0)
    def zoom_out(self):
        print('zoom out!')
        self.pr_roll.zoom_out()
        Clock.schedule_once(self.update, 0)
    def zoom_to(self, factor):
        self.pr_rooll.zoom_to(factor)
        Clock.schedule_once(self.update, 0)

