#region environment
import sys
sys.path.append(".\\")
#endregion
from piro.widgets.tracks import PrTrack, PrTracks

from kivy.graphics import Color, Line, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from piro.midi.clock import PrClock
from piro.env import PrEnv as Env



class PrRoll(BoxLayout):
    """
        PrRoll
        ======

        provides a pianoroll image for a given midi file.

        1. This object has only one function - drawing pianoroll canvas from a midi file.
        2. View functionality(zoom in/out, select track(s)...) is achieved by PrRollView class.
        3. A midi file must to be set when the object created.
        4. You can load another midi file with 'load_midi' public method.        
        
    """
    def __init__(self, midi, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoll, self).__init__(**kwargs)

        # midi
        self.midi = midi

        # props
        self.size_hint = (None, None)
        self.abs_width = 1280
        self.size = (1280, 1640)        

        # meters
        self.pips = None
        self.meters = None
        
        # notemap : [note(int)] { y / height }
        self.notemap = Env.ROLL_NOTEMAP()

        # instruction groups
        self.tracks = PrTracks()
        self.meterbars = {'bar':InstructionGroup()}
        self.timebar = InstructionGroup()

        # timebar object
        self._timebar = None

        # load_midi
        self.load_midi(midi)
    
    # public methods    
    def set_timebar(self, time=.0, x=None, tick=None):
        """draw a timebar at the given time(sec)"""
        if x:
            self._timebar.points = [x, 0, x, self.height]
            return x
        elif tick:
            x = self.pipt * tick
            self._timebar.points = [x, 0, x, self.height]
            return x
        elif self.pips:
            x = self.pips * time
            self._timebar.points = [x, 0, x, self.height]
            return x
        return None
    def get_timebar(self, time=None, tick=None):
        """get the current x-pos(pixel) of the timebar"""
        if time:
            if self.pips:
                return self.pips * time
        elif tick:
            if self.pipt:
                return self.pipt * time
        elif self._timebar:
            return self._timebar.points[0]
        return None
    def load_midi(self, midi):
        """reset the roll and load a new midi file"""
        self.midi = midi
        self.abs_width = ( Env.PIPQN / midi.ppqn ) * midi.totalticks
        self.size = (self.abs_width, 1640)
        self._draw_canvas()
        self._draw_meterbars()
        self._draw_notes()
        return self
    def hide_track(self, track_no):
        self.tracks.hide(track_no)
    def show_track(self, track_no):
        self.tracks.show(track_no)
    def get_tracks(self):
        return self.tracks

    # draw modules
    def _draw_timebar(self):
        # draw line
        self._timebar = Line(points=[0, 0, 0, self.height])

        # add timebar
        self.timebar.add(Color(*Env.ROLL_TIMEBAR_COLOR))
        self.timebar.add(self._timebar)         
    def _draw_meterbars(self):
        """ draw meterbars """
        # clear meterbars
        self.meterbars['bar'].clear()

        # midi
        midi = self.midi
        # get total length of the song
        totalticks = self.midi.get_totalticks()
        # pixel per tick
        ppt = self.width / totalticks
        # pixel per quarter note
        pipqn = midi.ppqn * ppt

        # store pips
        self.pips = self.abs_width / self.midi.get_length()
        self.pipt = self.abs_width / self.midi.get_length(ticks=True)  
        
        # color pick
        self.meterbars['bar'].add(Color(*Env.ROLL_METERBAR_COLOR))
        
        # meter info
        if not self.meters:
            tick = 0
            self.meters = []
            for msg in midi.midi_file.tracks[0]:
                tick += msg.time
                if msg.is_meta and msg.type == 'time_signature':
                    self.meters.append({'tick':tick, 'pixel':tick*ppt, 'msg':msg})
        
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
        while x <= self.width:
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

    def _draw_notes(self):
        """ draw noteoverlay """
        for tr_no, track in enumerate(self.midi.midi_file.tracks):
            self._draw_track(track, tr_no, Env.NOTE_COLOR[tr_no])

    def _draw_track(self, tr_midi, tr_no, tr_color):
        """ draw note for one track """
        # notes
        note_ons = {}

        # clear note overlay
        track = self.tracks.get(tr_no)
        if track:
            track.canvas.clear()

        # color pick
        track.paint(tr_color)

        # tick realted
        tick = 0
        totalticks = self.midi.get_totalticks()
        pptick = self.width / totalticks

        # print
        print( "{0:0>2} | {1: >5} | {2: <16} | {3: >20} | totalticks : {4:08}".format(tr_no, '', tr_midi.name, str(tr_color), totalticks))

        for msg in tr_midi:
            # time count
            tick += msg.time
            if not msg.is_meta:
                if msg.type == 'note_on' or msg.type == 'note_off':
                    # current x position
                    x = tick * pptick
                    # get the note history
                    note_on = note_ons.get(msg.note)
                    if note_on:
                        if msg.velocity == 0 or msg.type == 'note_off':                            
                            # calculate note info
                            note_off = self.notemap[msg.note]
                            note_off['width'] = x - note_on['x']
                            
                            # set rectangle props
                            pos = ( note_on['x'], note_on['y'] )
                            size = ( note_off['width'], note_off['height']-1 )

                            # draw rectangle
                            track.canvas.add(
                                Rectangle(pos=pos, size=size, group='Tr{0}'.format(tr_no))
                            )

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
    
    # draw kivy canvas
    def _draw_canvas(self):
        # roll width
        roll_width = self.width
      
        # clear canvas / notemap
        self.canvas.clear()

        #
        # background
        #
        # color pick - background
        self.canvas.add(Color(*Env.ROLL_BACKGROUND_COLOR))
        self.canvas.add(Rectangle(pos=(0, 0), size=self.size))

        #
        # ivory keys
        #
        # color pick - ivory
        self.canvas.add(Color(*Env.ROLL_IVORY_COLOR))

        # ivory key intervals
        ivory_intervals = [26, 26, 13, 26, 26, 26, 13]
        # y position
        pos_y, key_height = (0, 12)
        # nine octaves
        for i in range(Env.MAX_OCTAVES):
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
        self.canvas.add(Color(*Env.ROLL_EBONY_COLOR))

        # y position
        pos_y, key_height = (0, 12)
        # nine octaves
        for i in range(Env.MAX_OCTAVES):
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
        # self.meterbars is set here
        self.canvas.add(self.meterbars['bar'])

        #
        # note overlay - all
        #
        for ov in range(17):
            track = PrTrack(ov, True)
            self.tracks.add(ov, track)    
        self.canvas.add(self.tracks.draw())

        #
        # timebar
        #
        # self.timbar is set here
        self._draw_timebar()
        self.canvas.add(self.timebar)
        #print("roll:", self.pos, self.size, len(self.canvas.children))

if __name__ == '__main__':
    from kivy.app import App
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
            self.view = ScrollView(
                size_hint=(1, 1),
                bar_width=25,
                scroll_type=['bars'],
                effect_cls=ScrollEffect
            )
            
            self.view.add_widget(roll)
            self.layout.add_widget(self.view)

            PrClock.schedule_once(trigger, 0)
            # return
            return self.layout

    def trigger(instance):
        #midi.trigger(callback=play, callback_timebar=mypass)
        print ('roll size :', roll.size)
        print ('pipqn :', midi.ppqn * ( roll.width / midi.totalticks ))
    def play(i, msg, now):
        roll.play(msg)
    def mypass(i, now):
        pass

    midi = PrMidi(
        midi_filename='.\\midi\\midifiles\\fur-elise_short.mid',
        midi_portname='Microsoft GS Wavetable Synth 0')
    roll = PrRoll(midi)
    PrApp().run()