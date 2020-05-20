#region environment
import sys
sys.path.append(".\\")
#endregion
from kivy.graphics import PushMatrix, PopMatrix, Scale
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.core.window import Window
from kivy.clock import Clock
from piro.midi.helper import PrHelper

class PrRollView(ScrollView):
    """
        PrScrollView
        ============

        provides a container for PrRoll with these functions

        1. Scroll [horizontal/vertical]
        2. Zoom [in/out]
        3. You must set the child widget - it can be any kivy widget.
        
    """
    def __init__(self, child, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRollView, self).__init__(**kwargs)

        # kivy props
        self.size_hint=(1, 1)
        self.bar_width = 25
        self.scroll_type = ['bars']
        # No Effect for Scroll - kivy's scroll effect is buggy. I won't use it!
        self.effect_cls = ScrollEffect

        """ load child

            self.child : child object (any kivy widget)
            self.child_scale
            self.child_width : child width at scale 1.0
            self.child_height : child height at scale 1.0
        """
        self.child = None
        self.load_child(child)

    # public methods
    def get_x(self, x):
        return self.child_scale * x
    def load_child(self, child):
        if self.child:
            self.remove_widget(self.child)
        # members
        self.child = child
        # zoom in/out props
        self.child_width = self.child.width
        self.child_height = self.child.height

        self.child.canvas.before.clear()
        with child.canvas.before:
            PushMatrix()
            self.child_scale = Scale(1.0)

        self.child.canvas.after.clear()
        with child.canvas.after:
            PopMatrix()

        # add child
        self.add_widget(self.child)
        # return self
        return self
    
    # public methods - scroll
    def focus(self, x):
        """Scroll to the x"""
        if self.local_left <= x and x <= self.local_right:
            pass
        else:
            self.scroll_x = x / self.scroll_width          
            self.update_from_scroll()
    
    # public methods - zoom
    def zoom_in(self, factor=1.1):
        self._zoom_by(factor)
    def zoom_out(self, factor=0.9):
        self._zoom_by(factor)
    def zoom_to(self, factor):
        self.child_scale.x = factor
        self.child.width = self.child_width * factor

    @property
    def local_left(self):
        return self.to_local(self.x, 0)[0]
    @property
    def local_right(self):
        return self.to_local(self.width + self.x, 0)[0]
    @property
    def scroll_width(self):
        return self.child.width - self.width
    @property
    def scale(self):
        return self.child_scale

    # zoom by
    def _zoom_by(self, factor):
        self.child_scale.x *= factor
        self.child.width *= factor
    
if __name__ == '__main__':
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    from piro.midi.clock import PrClock
    from piro.midi.play import PrMidi
    from piro.widgets.roll import PrRoll
    class PrApp(App):
        """Main App"""
        def build(self):
            # window size / position
            Window.size = (1280, 1280)
            Window.left, Window.top = 30, 30

            # members
            self.layout = BoxLayout()
            self.layout.add_widget(view)

            PrClock.schedule_once(trigger, 0)
            # return
            return self.layout

    def trigger(instance):
        #midi.trigger(callback=play, callback_timebar=mypass)
        print ('roll size :', roll.size)
        print ('pipqn :', midi.ppqn * ( roll.width / midi.totalticks ))
        print ('zoom :', view.scale.x )
        print ('child :', view.child_width, view.child_height)
        print ('view :', view.size)
    def play(i, msg, now):
        roll.play(msg)
    def mypass(i, now):
        pass

    midi = PrMidi(
        midi_filename='.\\midi\\midifiles\\fur-elise_short.mid',
        midi_portname='Microsoft GS Wavetable Synth 0')
    roll = PrRoll(midi)
    view = PrRollView(roll)
    PrApp().run()