from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class PrRoll(BoxLayout):
    # constants
    _OCTAVES = 11

    """Roll Drawing"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoll, self).__init__(**kwargs)

        # props
        self.size_hint = (None, None)
        self.size = (1280, 1640)

        # canvas
        self.update_canvas()

    # public methods
    def update_canvas(self):
        # roll width
        roll_width = self.width

        # clear canvas
        self.canvas.clear()

        #
        # background
        #
        # color pick - background
        self.canvas.add(
            Color(0.8, 0.8, 1, 1.0))
        self.canvas.add(
            Rectangle(pos=(0, 0), size=self.size))

        #
        # ivory keys
        #
        # color pick - ivory
        self.canvas.add(
            Color(1, 1, 1, 1.0))

        # ivory key intervals
        ivory_intervals = [26, 26, 13, 26, 26, 26, 13]
        # y position
        pos_y, key_height = (0, 12)
        # nine octaves
        for i in range(self._OCTAVES):
            #pos_y -= 1        
            # iteration for octave
            for interval in ivory_intervals:
                self.canvas.add(
                    Rectangle(pos=(0, pos_y), size=(roll_width, key_height)))
                pos_y += interval

        #
        # ebony keys
        #
        # color pick - ebony
        self.canvas.add(
            Color(.8, .8, .8, 1.0))

        # y position
        pos_y, key_height = (0, 12)
        # nine octaves
        for i in range(self._OCTAVES):
            #pos_y -= 1
            # iteration for octave
            for idx, interval in enumerate(ivory_intervals):
                pos_y += interval
                if idx not in [2, 6]:
                    self.canvas.add(
                        Rectangle(pos=(0, pos_y - key_height - 1), size=(roll_width, key_height)))


        print("roll:", self.pos, self.size, len(self.canvas.children))
