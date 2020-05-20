#region environment
import sys
sys.path.append(".\\")
#endregion
from piro.widgets.zoomview import PrZoomView
from piro.widgets.roll import PrRoll
from piro.midi.helper import PrHelper

class PrRollView(PrZoomView):
    """
        PrRollView
        ============

        based on PrZoomView, this widget provides :

        1. automatically set child as PrRoll
        2. timebar select
        3. focus based on the given time
        4. convenient props for users
       
    """
    def __init__(self, midi, **kwargs):
        # create a PrRoll oject
        self.roll = PrRoll(midi)

        # make sure we aren't overriding any important functionality
        super(PrRollView, self).__init__(self.roll, **kwargs)

        # bind touch down
        self.roll.on_touch_down=self._roll_click


    # public methods
<<<<<<< HEAD
<<<<<<< HEAD
    def get_x(self, x):
=======
    def child_x(self, x):
>>>>>>> parent of 0bc183d... update
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

    # focus
    def focus(self, x):
        """Scroll to the x"""
        if self.local_left <= x and x <= self.local_right:
            pass
        else:
            self.scroll_x = x / self.scroll_width          
            self.update_from_scroll()

    # zoom in/out
    def zoom_in(self):
        self.child_scale.x *= 1.1
        self.child.width *= 1.1
    def zoom_out(self):
        self.child_scale.x /= 1.1
        self.child.width /= 1.1
    def zoom_to(self, factor):
        self.child_scale.x = factor
        self.child.width *= factor
<<<<<<< HEAD
    
=======
    def load(self, midi):
        """ load a new PrMidi object """
        roll = self.roll
        roll.load_midi(midi)
        self.load_child(roll)
    def set_timebar(self, time=None, x=None):
        if time:
            return self.child.set_timebar(time, x) * self.scale.x
        else:
            return self.child.set_timebar(time, x)

    # callbacks
    def _roll_click(self, touch):        
        self.set_timebar(self, x=touch.pos[0]/self.scale.x)            

>>>>>>> 8d3b0c18255f3655b68ded081a84d97b1202c99c
=======

>>>>>>> parent of 0bc183d... update
if __name__ == '__main__':
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    from piro.midi.clock import PrClock
    from piro.midi.play import PrMidi
    class PrApp(App):
        """Main App"""
        def build(self):
            # window size / position
            Window.size = (800, 600)
            Window.left, Window.top = 3100, 100

            # members
            self.layout = BoxLayout()
            self.layout.add_widget(view)

            # bind - keystrokes
            Window.bind(on_key_down=keydown)        

            PrClock.schedule_once(trigger, 0)
            # return
            return self.layout

    def trigger(instance):
        #midi.trigger(callback=play, callback_timebar=mypass)
        print ('roll size :', view.child.size)
        print ('pipqn :', midi.ppqn * ( view.child.width / midi.totalticks ))
        print ('zoom :', view.scale.x )
        print ('child :', view.child_width, view.child_height)
        print ('view :', view.size)
    def keydown(instance, key, keycode, text, modifiers):
        """Callback for KeyDown"""
        # zoom out
        if text == 'g':
            view.zoom_in()
        # zoom in
        elif text == 'h':
            view.zoom_out()
        # play
        elif text == ' ':
            PrHelper.msg('keydown','play')
        # reload
        elif text == 'w':            
            PrHelper.msg('keydown','rewind')
        # check
        elif text == 'c':
            PrHelper.msg('keydown', 'scroll_y', {
                "scroll_y":view.scroll_y,
                "scroll_x":view.scroll_x,
                "local_left":view.local_left,
                "local_right":view.local_right,
                "child_width":view.child_width,
                "child_height":view.child_height,
                "child_scale":view.scale }
            )                
        return True

    midi = PrMidi(
        midi_filename='.\\midi\\midifiles\\fur-elise_short.mid',
        midi_portname='Microsoft GS Wavetable Synth 0')
    view = PrRollView(midi)
    PrApp().run()