from kivy.graphics import Color, Line, Rectangle, PushMatrix, PopMatrix
from kivy.graphics import Translate, Rotate, Scale
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from piro.midi.clock import PrClock

class PrRoll(BoxLayout):
    """Roll Drawing"""

    # constants
    _OCTAVES = 11
    
    # init
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoll, self).__init__(**kwargs)

        # midi
        self.midi = None

        # props
        self.size_hint = (None, None)
        self.roll_width = 1280
        self.size = (1280, 1640)        
        self.scale = None

        # meters
        self.ttl = None
        self.pips = None
        self.meters = None
        self.meter_width = 1
        
        # notemap : [note(int)] { x / y / height }
        self.notemap = []
        self.set_notemap()

        # instruction groups
        self.notes = {'all':InstructionGroup()}
        self.meterbars = {'bar':InstructionGroup()}
        self.timebar = InstructionGroup()

        # canvas
        self.draw_canvas()
    def set_notemap(self):
        """ set notemap """
        self.notemap = []

        # pos_y / interval
        pos_y = 0
        interval = 13

        for i in range(128):                  
            self.notemap.append({
                'y': pos_y,
                'height': interval
            })
            pos_y += interval
    
    # draw modules
    def draw_timebar(self, time=.0):
        if self.pips:
            # draw rectangle
            x = time * self.pips
            self.timebar.clear()
            self.timebar.add(
                Line(points=[x, 0, x, self.height])
            )         

    def draw_meterbars(self, midi=None):
        """ draw meterbars """
        # pass on conditions
        if len(self.notemap) == 0:
            return
        elif not midi:
            if self.midi:
                midi = self.midi
            else:
                return

        # update self.midi
        if midi:
            self.midi = midi
        
        # clear meterbars
        self.meterbars['bar'].clear()
        # get total length of the song
        if not self.ttl:            
            self.ttl = self.midi.length
        # second per quarter note
        spqn = midi.ppqn * midi.spt
        # pixel per second
        if not self.pips:
            self.pips = self.roll_width / self.ttl
        # pixel per quarter note
        pipqn = spqn * self.pips
        
        # color pick
        self.meterbars['bar'].add(Color(0.3, 0.3, 0.3, 1))
        
        # meter info
        if not self.meters:
            t = .0
            self.meters = []
            for msg in midi.midi_file.tracks[0]:
                t += msg.time
                if msg.is_meta and msg.type == 'time_signature':
                    self.meters.append({'tick':t, 'sec':t*midi.spt, 'pixel':t*midi.spt*self.pips, 'msg':msg})
        
        # variables for drawing
        meter_iter = iter(self.meters)
        x = .0
        num, denom = (4, 4)
        pibar = pipqn * num * (4/denom)

        # load the first meter if it exists
        try:
            next_meter = next(meter_iter)
        except StopIteration:
            next_meter = None

        # main iteration
        while x <= self.roll_width:
            # draw rectangle
            self.meterbars['bar'].add(
                Line(points=[x, 0, x, self.height], group='bar')
            )

            # if next meter exists
            if next_meter:
                # if it's the right time to swith to the new meter
                if x >= next_meter['pixel']:
                    msg = next_meter['msg']
                    num, denom = (msg.numerator, msg.denominator)
                    pibar = pipqn * num * (4/denom)
                    try:
                        next_meter = next(meter_iter)
                    except StopIteration:
                        next_meter = None
            
            x += pibar

    def draw_notes(self, midi=None):
        """ draw noteoverlay """
        # pass on conditions
        if len(self.notemap) == 0:
            return
        elif not midi:
            if self.midi:
                midi = self.midi
            else:
                return

        # notes
        note_ons = {}

        # self.midi
        self.midi = midi

        # clear note overlay
        self.notes['all'].clear()

        # get total length of the song
        ttl = self.midi.length

        # time(seconds)
        time = .0
        ppt = self.width / ttl
        print(ppt)
        # color pick
        self.notes['all'].add(Color(0.5, 0.5, 0.5, 1))

        clock = PrClock()
        clock.set_timer(1)

        totalticks = self.midi.get_ticklength()
        pptick = self.width / totalticks

        clock.set_timer(1)
        n_obj = 0
        for msg in midi.midi_file.tracks[1]:
            # time count
            time += msg.time
            if not msg.is_meta:
                if msg.type == 'note_on':
                    # current x position
                    x = time * pptick
                    # get the note history
                    note_on = note_ons.get(msg.note)
                    if note_on:
                        if msg.velocity == 0:                            
                            # calculate note info
                            note_off = self.notemap[msg.note]
                            note_off['width'] = x - note_on['x']
                            
                            # set rectangle props
                            pos = ( note_on['x'], note_on['y'] )
                            size = ( note_off['width'], note_off['height']-1 )

                            # draw rectangle
                            self.notes['all'].add(
                                Rectangle(pos=pos, size=size, group='all')
                            )
                            n_obj += 1

                            # clear note_on
                            note_ons[msg.note] = None
                        else:
                            # another note_on happens without note_off
                            # so, do nothing when velocity > 0
                            pass
                    else:
                        if msg.velocity > 0:
                            #  new note_on, so just store the value
                            note_on = self.notemap[msg.note]
                            note_on['x'] = x
                            note_ons[msg.note] = note_on
                        else:
                            # note_off without note_on
                            # so, do nothing
                            pass
        print("draw note[mainloop] : ",clock.elapsed(1))
        print("object# :", n_obj)

    # zoom in/out
    def zoom_in(self):        
        self.scale.x *= 1.1
        # for scrollview effect
        self.width *= 1.1
    def zoom_out(self):
        self.scale.x /= 1.1
        # for scrollview effect
        self.width /= 1.1

    # draw canvas
    def draw_canvas(self):
        # roll width
        roll_width = self.width
      
        # clear canvas / notemap
        self.canvas.clear()

        # 
        # before canvas
        #
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            self.scale = Scale(1.0)

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
        # meterbars
        #
        self.canvas.add(self.meterbars['bar'])

        #
        # note overlay - all
        #
        self.canvas.add(self.notes['all'])

        #
        # timebar
        #
        self.canvas.add(Color(0.1, 0.1, 0.1, 1))
        self.canvas.add(self.timebar)

        #
        # after canvas
        #
        self.canvas.after.clear()
        with self.canvas.after:
            PopMatrix()

        print("roll:", self.pos, self.size, len(self.canvas.children))
