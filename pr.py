# Import kivy config class
from kivy.config import Config
# setup kivy clock as 'free_only'
Config.set('kivy', 'kivy_clock', 'free_only')

# kivy modules
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# piro modules
import piro.widgets as widgets

# piro classes
from piro.midi.play import PrMidi
from piro.midi.clock import PrClock

class PrRoot(BoxLayout):
    """Root Widget"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoot, self).__init__(**kwargs)

        # props
        self.orientation = 'vertical'

        # midi
        self.midi = PrMidi(
            midi_filename='.\\midi\\midifiles\\waldstein_1.mid',
            midi_portname='Microsoft GS Wavetable Synth 0')
        self.now = .0
        
        # menu widget
        self.pr_menu = widgets.PrMenu()        
        # piano-roll layout
        self.pr_pianoroll_view = BoxLayout(orientation='horizontal')
        # piano-roll layout contains 2 scrollviews - piano/roll
        self.pr_piano_view = widgets.PrPianoView()
        self.pr_roll_view = widgets.PrRollView()

        # binds
        self.pr_roll_view.bind(scroll_y=self._roll_scroll_sync)
        self.pr_piano_view.bind(scroll_y=self._piano_scroll_sync)
        self.pr_menu.btn_play.bind(on_press=self._menu_button_play)
        self.pr_menu.btn_test.bind(on_press=self._menu_button_test)

        # children
        self.pr_pianoroll_view.add_widget(self.pr_piano_view)
        self.pr_pianoroll_view.add_widget(self.pr_roll_view)
        self.add_widget(self.pr_menu)
        self.add_widget(self.pr_pianoroll_view)

    # callbacks
    def _menu_button_play(self, instance):
        """Midi Play Button"""
        print(instance)
        btn = instance
        if btn.text == 'Play':
            btn.text = 'Stop'
            self.midi.reload()
            self.midi.trigger(
                callback=self._play_callback,
                callback_timebar=self._play_callback_timebar
            )
        else:
            btn.text = 'Play'
            self.midi.stop()
            self.now = .0
    def _play_callback_timebar(self, instance, now):
        """Callback for Timebar - !!! frequent calls !!!"""
        roll = self.pr_roll_view.pr_roll

        if now - self.now > 0.075:
            self.now = now
            roll.draw_timebar(now)

    def _play_callback(self, instance, msg, now):
        '''Callback for Play'''
        piano = self.pr_piano_view.pr_piano
        roll = self.pr_roll_view.pr_roll

        # draw note_on/off status
        if msg.type == 'note_on':
            if msg.velocity == 0:
                print(msg.note, 'is off @', now)
                piano.note(msg.note, on=False)
                piano.update_keyoverlay()
            else:
                print(msg.note, 'is on  @', now)
                piano.note(msg.note, on=True)
                piano.update_keyoverlay()
        elif msg.type == 'note_off':
            print(msg.note, 'is off @', now)
            piano.note(msg.note, on=False)
            piano.update_keyoverlay()
        else:
            pass
            
    def _menu_button_test(self, instanace):
        """Test Button"""
        piano = self.pr_piano_view.pr_piano
        roll = self.pr_roll_view.pr_roll

        prClock = PrClock()

        prClock.set_timer(1)
        roll.draw_meterbars(midi=self.midi)
        print('draw_meterbars : ', prClock.elapsed(1))
        prClock.set_timer(1)
        roll.draw_notes(midi=self.midi)
        print('draw_notes : ', prClock.elapsed(1))

    def _roll_scroll_sync(self, instance, scroll_y):
        """Sync Scroll between piano and roll views"""
        self.pr_piano_view.scroll_y = scroll_y

    def _piano_scroll_sync(self, instance, scroll_y):
        """Sync Scroll between piano and roll views"""
        self.pr_roll_view.scroll_y = scroll_y


class PrApp(App):
    """Main App"""
    def build(self):
        # window size / position
        Window.size = (1024, 768)
        Window.left, Window.top = 300, 200

        # members
        self.pr_root = PrRoot()

        # binds
        self.pr_root.bind(size=self._update_size)

        # return
        return self.pr_root

    # bind callbacks
    def _update_size(self, instance, value):
        print("instance size:",instance.size)


if __name__ == '__main__':
    PrApp().run()
