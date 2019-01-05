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

class PrRoot(BoxLayout):
    """Root Widget"""
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoot, self).__init__(**kwargs)

        # props
        self.orientation = 'vertical'

        # midi
        self.midi = PrMidi(
            midi_filename='.\\midi\\midifiles\\fur-elise.mid',
            midi_portname='Microsoft GS Wavetable Synth 0')
        
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

    def _menu_button_play(self, instance):
        """Midi Play Button"""
        print(instance)
        btn = instance
        if btn.text == 'Play':
            btn.text = 'Stop'
            self.midi.reload()
            self.midi.trigger(callback=self._play_callback)
        else:
            btn.text = 'Play'
            self.midi.stop()

    def _play_callback(self, instance, msg, now):
        '''Callback for Play'''
        piano = self.pr_piano_view.pr_piano

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

        #piano.pressed_keys = []
        #piano.update_canvas()
        #piano.update_groups()
        #print(piano.keypressed)
        print(roll.notemap)
        roll.draw_noteoverlay(midi=self.midi)

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
        Window.size = (300, 300)
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
