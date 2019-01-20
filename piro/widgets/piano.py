#region environment
import sys
sys.path.append(".\\")
# Import kivy config class
from kivy.config import Config
# setup kivy clock as 'free_only'
Config.set('kivy', 'kivy_clock', 'free_only')
#endregion
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.core.text import Label as CoreLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from piro.env import PrEnv as Env
from piro.midi.clock import PrClock

class PrPiano(BoxLayout):
    """
        PrPiano
        =======

        provides a horizontal piano image with key on/off visual effect

        1. The main goal of this object is just drawing a piano keyboard
        2. Addtionally, you can set key on/off effect with 'play' public method

    """
    # init
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrPiano, self).__init__(**kwargs)

        # props
        self.size_hint = (None, None)
        self.size = (150, 1640)

        """ keys are ordered by their drawing sequence in canvas
            use keymap to find the key for the target note
            ex) self.keys[self.keymap[3]]  => returns the key object of D#0
        """
        self.keys = []        
        self.keymap = Env.PNO_KEYMAP()

        # canvas init
        self._draw_canvas()

    # public methods
    def play(self, msg):
        """draw note_on/off status. accept mido message"""
        if msg.type == 'note_on':
            if msg.velocity == 0:
                self._note(note=msg.note, on=False)
            else:
                self._note(note=msg.note, on=True)
        elif msg.type == 'note_off':
            self._note(note=msg.note, on=False)
        else:
            pass
    def stop(self):
        """ stop all the playing notes """
        for key in self.keys:
            if key['pressed']:
                self._note(key=key, on=False)

    @property
    def _lastkey(self):
        """ returns the last object of self.keys """
        if len(self.keys) > 0:
            return self.keys[len(self.keys)-1] 
        else:
            return None
    # set note
    def _note(self, on, note=0, key=None):
        if not key:
            key = self.keys[self.keymap[note]]

        if on and not key['pressed']:
            key['color'].rgba = Env.PNO_PRESSED_COLOR
            key['pressed'] = True
        elif not on and key['pressed']:
            if key['type'] == 'ivory':
                key['color'].rgba = Env.PNO_IVORY_COLOR
            elif key['type'] == 'ebony':
                key['color'].rgba = Env.PNO_EBONY_COLOR
            else:
                pass
            key['pressed'] = False
    
    # draw kivy canvas
    def _draw_canvas(self):
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
        # ivory key intervals
        ivory_intervals = [19, 25, 18, 19, 25, 25, 18]
        pos_octave = []
        # y position, key idx_key
        pos_y = 1
        idx_key = 0
        # iteration for octave
        for i in range(Env.MAX_OCTAVES):
            # position for the octave start
            pos_octave.append(pos_y)
            for interval in ivory_intervals:
                self.keys.append({'type':'ivory', 'pressed':False, 'color':Color(*Env.PNO_IVORY_COLOR)})
                self.canvas.add(self._lastkey['color'])
                self.canvas.add(Rectangle(pos=(0, pos_y), size=(90, interval)))
                pos_y += interval + 1
                idx_key += 1

        #
        # ebony keys
        #
        # color pick - ebony
        self.canvas.add(Color(0, 0, 0, 1.0)) 

        # ivory key intervals
        ebony_interval = 12
        # y position
        pos_y = 1
        # iteration for octave
        for i in range(Env.MAX_OCTAVES):
            for idx, interval in enumerate(ivory_intervals):
                pos_y += interval + 1
                if idx not in [2, 6]:
                    self.keys.append({'type':'ebony', 'pressed':False, 'color':Color(*Env.PNO_EBONY_COLOR)})
                    self.canvas.add(self._lastkey['color'])
                    self.canvas.add(Rectangle(pos=(0, pos_y-6), size=(60, ebony_interval)))                
                    idx_key += 1

        #
        # octave labels
        #
        self.canvas.add(Color(1, 1, 1, 1.0))
        for i, y in enumerate(pos_octave):
            self.canvas.add(Rectangle(pos=(0, y-5.5), size=(30, 11)))
                
        # set color
        self.canvas.add(Color(0, 0, 0, 1.0))
        # draw
        for i, y in enumerate(pos_octave):
            label = CoreLabel(text="C %d"%i, font_size=11)
            label.refresh()
            text = label.texture
            self.canvas.add(Rectangle(pos=(2, y-text.height/2), size=text.size, texture=text))

        print("piano:", self.pos, self.size, len(self.canvas.children), idx_key)

if __name__ == '__main__':
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.scrollview import ScrollView
    from kivy.clock import Clock
    from piro.midi.play import PrMidi
    class PrApp(App):
        """Main App"""
        def build(self):
            # window size / position
            Window.size = (150, 1280)
            Window.left, Window.top = 30, 30

            # members
            self.layout = BoxLayout()
            self.view = ScrollView(
                size_hint=(None, 1),
                width=98,
                bar_width=5,
                scroll_type=['bars']
            )
            
            self.view.add_widget(pno)
            self.layout.add_widget(self.view)

            PrClock.schedule_once(trigger, 0)

            # return
            return self.layout

    def trigger(instance):        
        midi.trigger(callback=play, callback_timebar=mypass)
    def play(i, msg, now):
        pno.play(msg)
    def mypass(i, now):
        pass

    midi = PrMidi(
        midi_filename='.\\midi\\midifiles\\fur-elise_short.mid',
        midi_portname='Microsoft GS Wavetable Synth 0')
    pno = PrPiano()
    PrApp().run()