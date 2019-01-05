from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class PrRoll(BoxLayout):
    # constants
    _OCTAVES = 11

    """Roll Drawing"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoll, self).__init__(**kwargs)

        # midi
        self.midi = None

        # props
        self.size_hint = (None, None)
        self.size = (1280, 1640)        

        # notes
        self.notemap = []
        self.noteoverlay = {'all':InstructionGroup()}

        # set notemap
        self._set_notemap()

        # canvas
        self.draw_canvas()
        

    # private methods
    def _set_notemap(self):
        self.notemap = []

        # pos_y / interval
        pos_y = 0
        interval = 12

        for i in range(128):                  
            self.notemap.append({
                'y': pos_y,
                'height': interval
            })
            pos_y += interval

    # public methods
    def draw_noteoverlay(self, midi=None):
        # pass on conditions
        if len(self.notemap) == 0:
            return
        elif not midi:
            if self.midi:
                midi = self.midi
            else:
                return

        # self self.midi
        self.midi = midi

        # clear note overlay
        self.noteoverlay['all'].clear()

        # get total length of the song
        ttl = midi.get_length()
        # time(seconds)
        time = .0
        ppt = self.width / ttl

        # color pick
        self.noteoverlay['all'].add(Color(1, 0.5, 0.5, 1))

        for msg in midi.midi_file:
            if not msg.is_meta:
                if msg.type == 'note_on':
                    x = time * ppt
                    # print (msg, x, len(self.notemap))
                    note = self.notemap[msg.note]                    
                    self.noteoverlay['all'].add(
                        Rectangle(pos=(x, note['y']), size=(5, note['height']), group='all')
                    )
            time += msg.time            
    
    def draw_canvas(self):
        # roll width
        roll_width = self.width

        # clear canvas / notemap
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
                    Rectangle(pos=(0, pos_y), size=(roll_width, key_height))
                )
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
                        Rectangle(pos=(0, pos_y - key_height - 1), size=(roll_width, key_height))
                    )
        
        #
        # note overlay - all
        #
        self.canvas.add(self.noteoverlay['all'])

        print("roll:", self.pos, self.size, len(self.canvas.children))
