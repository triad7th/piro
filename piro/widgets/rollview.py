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

        based on PrZoomView, this widget privdes :

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
        self.roll.bind(on_touch_down=self.on_touch_down)


    # public methods
    def load(self, midi):
        """ load a new mido object """
        roll = self.roll
        roll.load_midi(midi)
        self.load_child(roll)

    def set_timebar(self, time=None, x=None):
        self.child.set_timebar(time, x)

    # callbacks
    def on_touch_down(self, touch):
        print(touch, view.local_left, view.local_right)
        self.set_timebar(self, x=touch.pos[0]/self.scale.x)
        

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
            Window.size = (300, 200)
            Window.left, Window.top = 30, 1000

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
        print ('roll size :', roll.size)
        print ('pipqn :', midi.ppqn * ( roll.width / midi.totalticks ))
        print ('zoom :', view.scale.x )
        print ('child :', view.child_width, view.child_height)
        print ('view :', view.size)
    def play(i, msg, now):
        roll.play(msg)
    def mypass(i, now):
        pass
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
    roll = view.child
    PrApp().run()