from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PrMenu(BoxLayout):
    """Menu Widget"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrMenu, self).__init__(**kwargs)

        # props
        self.size_hint = (1, None)
        self.height = 50
        self.orientation = 'horizontal'
        
        # children declare
        self.btn_play = Button(text='Play', size_hint=(None, 1), width=150)
        self.btn_test = Button(text='Test', size_hint=(None, 1), width=150)

        # children add
        self.add_widget(self.btn_play)
        self.add_widget(self.btn_test)