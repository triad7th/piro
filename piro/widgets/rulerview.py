from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from piro.widgets.piano import PrPiano

class PrRulerView(ScrollView):
    """Ruler"""
    def __init__(self, roll, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRulerView, self).__init__(**kwargs)

        # props
        self.size_hint = (1, None)
        self.height = 100
        self.bar_width = 0
        self.scroll_type = ['bars']
        self.visible = True

        self.roll = roll
        
    # public methods
    
    # callbacks
    