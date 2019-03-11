#region environment
#import sys
#sys.path.append(".\\")
#endregion
from kivy.graphics.instructions import InstructionGroup

class PrTrack:
    """
        PrTrack
        ========

        provides an object which manages track instruction group

        1. Name of track
        1. Instruction group
        2. Visible parameter
    """
    def __init__(self, name='', visibility=False):
        self.canvas = None
        self.name = None
        self.visible = None

        self.new(name, visibility)

    def new(self, name='', visibility=False):
        self.canvas = InstructionGroup()
        self.name = name
        self.visible = visibility
        
class PrTracks:
    """
        PrTracks
        ========

        provides object which manage track instruction groups

        1. Container instruction group for canvas
        2. List of PrTracks
        3. show/hide tracks
        4. z-order handling
        
    """
    def __init__(self):
        self.container = InstructionGroup()
        self.tracks = {}
        
    def get(self, idx):
        if idx in self.tracks:
            return self.tracks[idx]
    
    def add(self, idx, track):
        self.tracks[idx] = track
        self.container.add(track.canvas)

    def remove(self, idx):
        self.container.remove(self.tracks[idx].canvas)
        self.tracks[idx] = None

    def show(self, idx):
        track = self.tracks[idx]
        if track:
            if self.tracks[idx].visible == False:
                self.container.add(track.canvas)
                track.visible = True

    def hide(self, idx):
        track = self.tracks[idx]
        if track:
            if self.tracks[idx].visible:
                self.container.remove(track.canvas)
                track.visible = False

    def draw(self):
        self.container.clear()
        for key in self.tracks:
            self.container.add(self.tracks[key].canvas)        
        return self.container

if __name__ == '__main__':
    from kivy.app import App
    from kivy.graphics import Color, Line, Rectangle
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.image import Image
    from piro.midi.clock import PrClock
    from kivy.core.window import Window
    from kivy.uix.scrollview import ScrollView
    from kivy.effects.scroll import ScrollEffect
    from piro.midi.play import PrMidi
    class PrApp(App):
        """Main App"""
        def build(self):
            # window size / position
            Window.size = (1280, 600)
            Window.left, Window.top = 3100, 30

            # members
            self.layout = BoxLayout()
            test = InstructionGroup()
            a = PrTracks()
            a.add(PrTrack('', True))

            self.layout.canvas.add(Rectangle(pos=(100, 100), size=(100, 100)))
            PrClock.schedule_once(trigger, 0)
            # return
            return self.layout

    def trigger(instance):
        pass
    
    PrApp().run()