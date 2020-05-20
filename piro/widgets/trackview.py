from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from piro.widgets.piano import PrPiano

class PrTrackView(ScrollView):
    """Piano ScrollView"""
    def __init__(self, roll, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrTrackView, self).__init__(**kwargs)

        # props
        self.size_hint = (None, 1)
        self.width = 150
        self.bar_width = 0
        self.scroll_type = ['bars']
        self.visible = True

        self.roll = roll
        self.pr_tracks = roll.get_tracks()
        self.buttons = []

        # members
        self.container = BoxLayout(size_hint=(None, None), size=(150, 800), orientation='vertical')

        # buttons
        for i in self.pr_tracks.tracks:
            track = self.pr_tracks.tracks[i]
            button = Button(text="{0}|{1}".format(track.name,track.visible))            
            self.buttons.append(button)
            self.container.add_widget(button)            
            self.buttons[i].bind(on_press=self._on_press)

        # child layout
        self.add_widget(self.container)

    # public methods
    def refresh(self):
        for i in self.pr_tracks.tracks:
            track = self.pr_tracks.tracks[i]
            self.buttons[i].text = "{0}|{1}".format(track.name,track.visible)            

    # callbacks
    def _on_press(self, instance):
        no = self.buttons.index(instance)
        track = self.pr_tracks.tracks[no]
        if track.visible:
            self.roll.hide_track(no)
        else:
            self.roll.show_track(no)
        self.refresh()

                    

    
