from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from piro.widgets.piano import PrPiano

class PrPianoView(ScrollView):
    """Piano ScrollView"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrPianoView, self).__init__(**kwargs)

        # props
        self.size_hint = (None, 1)
        self.width = 98
        self.bar_width = 0
        self.scroll_type = ['bars']

        # members
        self.pr_piano = PrPiano()

        # child layout
        self.add_widget(self.pr_piano)