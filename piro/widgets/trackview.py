from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from piro.widgets.piano import PrPiano

class PrTrackView(ScrollView):
    """Piano ScrollView"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrTrackView, self).__init__(**kwargs)

        # props
        self.size_hint = (None, 1)
        self.width = 150
        self.bar_width = 0
        self.scroll_type = ['bars']
        self.visible = True

        # members
        self.pr_tracks = BoxLayout(size_hint=(None, None), size=(150, 1640))

        # child layout
        self.add_widget(self.pr_tracks)