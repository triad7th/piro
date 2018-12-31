from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.core.text import Label as CoreLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class PrPiano(BoxLayout):
    """Piano Body Drawing"""
    # constants
    _OCTAVES = 11
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrPiano, self).__init__(**kwargs)

        # props
        self.size_hint = (None, None)
        self.size = (150, 1640)

        # keys
        self.pressed_keys = {}
        self.keymap = []

        # keymap
        self._set_keymap()

        # canvas
        self.update_canvas()

        # children
        #self.add_widget(Image(source='./Source/PianoRoll/images/smile2.png', keep_ratio=False, allow_stretch=True))
    # private methods
    def _set_keymap(self):
        # set reverse keymap
        rev_keymap = []
        for octave in range(self._OCTAVES):
            for ivory in [0, 2, 4, 5, 7, 9, 11]:
                rev_keymap.append(octave*12+ivory)
        for octave in range(self._OCTAVES):
            for ebony in [1, 3, 6, 8, 10]:
                rev_keymap.append(octave*12+ebony)
        
        # reverse it to set keymap
        self.keymap = []
        for idx in range(len(rev_keymap)):
            self.keymap.append(rev_keymap.index(idx))

        print (self.keymap)            

    # public methods
    def note(self, note, on):
        self.pressed_keys["%d"%self.keymap[note]] = on

    def update_canvas(self):
        # clear canvas
        self.canvas.clear()

        #
        # background
        #
        # color pick - background
        self.canvas.add(Color(.3, .3, .3, 1.0))
        self.canvas.add(Rectangle(pos=(0, 0), size=self.size))

        #
        # ivory keys
        #
        # color pick - ivory
        self.canvas.add(
            Color(1, 1, 1, 1.0)) 

        # ivory key intervals
        ivory_intervals = [19, 25, 18, 19, 25, 25, 18]
        pos_octave = []
        # y position, key idx_key
        pos_y = 1
        idx_key = 0
        # iteration for octave
        for i in range(self._OCTAVES):
            # position for the octave start
            pos_octave.append(pos_y)
            for interval in ivory_intervals:
                self.canvas.add(
                    Rectangle(pos=(0, pos_y), size=(90, interval)))
                pos_y += interval + 1
                idx_key += 1

        #
        # ebony keys
        #
        # color pick - ebony
        self.canvas.add(
            Color(0, 0, 0, 1.0)) 

        # ivory key intervals
        ebony_interval = 12
        # y position
        pos_y = 1
        # iteration for octave
        for i in range(self._OCTAVES):
            for idx, interval in enumerate(ivory_intervals):
                pos_y += interval + 1
                if idx not in [2, 6]:
                    self.canvas.add(
                        Rectangle(pos=(0, pos_y-6), size=(60, ebony_interval)))
                    idx_key += 1

        #
        # octave labels
        #
        self.canvas.add(Color(1, 1, 1, 1.0))
        for i, y in enumerate(pos_octave):
            self.canvas.add(
                Rectangle(pos=(0, y-5.5), size=(30, 11)))   
        # set color
        self.canvas.add(Color(0, 0, 0, 1.0))
        # draw
        for i, y in enumerate(pos_octave):
            label = CoreLabel(text="C %d"%i, font_size=11)
            label.refresh()
            text = label.texture
            self.canvas.add(
                Rectangle(pos=(2, y-text.height/2), size=text.size, texture=text))

        #
        # keypressed overlay
        #
        self.canvas.add(self.keypressed_group())        

        print("piano:", self.pos, self.size, len(self.canvas.children), idx_key)
