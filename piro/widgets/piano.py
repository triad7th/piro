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

class PrPiano(BoxLayout):
    """Piano Body Drawing"""
    # init
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrPiano, self).__init__(**kwargs)

        # props
        self.size_hint = (None, None)
        self.size = (150, 1640)

        # keys
        self.keypressed = {0:False,}
        self.keymap = []
        self.keyoverlay = {'ebony':InstructionGroup(), 'ivory':InstructionGroup()}

        # keymap
        self._set_keymap()

        # canvas init
        self.draw_canvas()

    # public methods
    def play(self, msg):
        # draw note_on/off status
        if msg.type == 'note_on':
            if msg.velocity == 0:
                self.note(msg.note, on=False)
                self.update_keyoverlay()
            else:
                self.note(msg.note, on=True)
                self.update_keyoverlay()
        elif msg.type == 'note_off':
            self.note(msg.note, on=False)
            self.update_keyoverlay()
        else:
            pass
    def stop(self):
        """ stop all the playing notes """
        self.keypressed = {0:False,}
        self.update_keyoverlay()

    # set note
    def note(self, note, on):
        self.keypressed[self.keymap[note]] = on
    # 1:1 matching of key and actual order of drawing
    def _set_keymap(self):
        # set reverse keymap
        rev_keymap = []
        for octave in range(Env.MAX_OCTAVES):
            for ivory in [0, 2, 4, 5, 7, 9, 11]:
                rev_keymap.append(octave*12+ivory)
        for octave in range(Env.MAX_OCTAVES):
            for ebony in [1, 3, 6, 8, 10]:
                rev_keymap.append(octave*12+ebony)
        
        # reverse it to set keymap
        self.keymap = []
        for idx in range(len(rev_keymap)):
            self.keymap.append(rev_keymap.index(idx))
        #print (self.keymap)            

    # keyoverlay
    def draw_keyoverlay(self):
        self.keyoverlay['ebony'].clear()
        self.keyoverlay['ivory'].clear()

        # color pick
        self.keyoverlay['ivory'].add(Color(0, 1, 1, 0.8))

        #
        # keypressed indicator draw
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
                if self.keypressed.get(idx_key, False):
                    self.keyoverlay['ivory'].add(Rectangle(pos=(0, pos_y), size=(90, interval), group='ivory'))
                pos_y += interval + 1
                idx_key += 1

        # color pick
        self.keyoverlay['ebony'].add(Color(0, 1, 1, 0.8))

        #
        # ebony keys
        #
        # ivory key intervals
        ebony_interval = 12
        # y position
        pos_y = 1
        # iteration for octave
        for i in range(Env.MAX_OCTAVES):
            for idx, interval in enumerate(ivory_intervals):
                pos_y += interval + 1
                if idx not in [2, 6]:
                    if self.keypressed.get(idx_key, False):
                        self.keyoverlay['ebony'].add(Rectangle(pos=(0, pos_y-6), size=(60, ebony_interval), group='ebony'))
                    idx_key += 1
    def update_keyoverlay(self):
        self.keyoverlay['ebony'].clear()
        self.keyoverlay['ivory'].clear()
        self.draw_keyoverlay()

    # canvas
    def draw_canvas(self):
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
        for i in range(Env.MAX_OCTAVES):
            # position for the octave start
            pos_octave.append(pos_y)
            for interval in ivory_intervals:
                self.canvas.add(
                    Rectangle(pos=(0, pos_y), size=(90, interval)))
                pos_y += interval + 1
                idx_key += 1

        #
        # keypressed overlay - ivory
        #
        self.draw_keyoverlay()
        self.canvas.add(self.keyoverlay['ivory'])

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
        for i in range(Env.MAX_OCTAVES):
            for idx, interval in enumerate(ivory_intervals):
                pos_y += interval + 1
                if idx not in [2, 6]:
                    self.canvas.add(
                        Rectangle(pos=(0, pos_y-6), size=(60, ebony_interval)))
                    idx_key += 1

        #
        # keypressed overlay - ebony
        #
        self.canvas.add(self.keyoverlay['ebony'])

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
            Window.size = (150, 300)
            Window.left, Window.top = 0, 600

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

            Clock.schedule_once(trigger, 0)

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