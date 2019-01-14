#region environment
# Import kivy config class
from kivy.config import Config
# setup kivy clock as 'free_only'
Config.set('kivy', 'kivy_clock', 'free_only')
#endregion
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# piro modules
import piro.widgets as widgets

# piro classes
from piro.midi.play import PrMidi
from piro.midi.clock import PrClock

class PrRoot(BoxLayout):
    """Root Widget"""
    # init
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoot, self).__init__(**kwargs)

        # props
        self.midi = PrMidi(
            midi_filename='.\\midi\\midifiles\\fur-elise_short.mid',
            midi_portname='Microsoft GS Wavetable Synth 0')
        self.orientation = 'vertical'
        self.now = .0
        self.bar_x = .0

        # widgets factory / bind
        self.widget_factory()
        self.widget_bind()

        # bind - keystrokes
        Window.bind(on_key_up=self._keyup)
        Window.bind(on_key_down=self._keydown)        

        # draw roll
        Clock.schedule_once(self.draw_roll, 0)
   
    # widget factory / bind / draw
    def widget_factory(self):
        """        
            self.pr_menu
            self.pr_view
                self.pr_piano_view
                self.pr_roll_view
        """
        # big widgets
        self.pr_menu = widgets.PrMenu()     
        self.pr_view = BoxLayout(orientation='horizontal')
        # small widgets
        if self.pr_view:
            self.pr_piano_view = widgets.PrPianoView()
            self.pr_roll_view = widgets.PrRollView()

        # add small widgets
        if self.pr_view:
            self.pr_view.add_widget(self.pr_piano_view)
            self.pr_view.add_widget(self.pr_roll_view)
        # add big widgets
        self.add_widget(self.pr_menu)
        self.add_widget(self.pr_view)
    def widget_bind(self):
        """
            sync y-scroll for piano / roll
            button clicks for menu
        """
        # bind - piano/roll y sync
        self.pr_roll_view.bind(scroll_y=self._roll_scroll_sync)
        self.pr_piano_view.bind(scroll_y=self._piano_scroll_sync)
        self.pr_roll_view.bind(scroll_x=self._scroll_x)

        # bind - buttons
        self.pr_menu.btn_play.bind(on_press=self._menu_button_play)
        self.pr_menu.btn_test.bind(on_press=self._menu_button_test)
    def draw_roll(self, instance):
        # widgets
        rollview = self.pr_roll_view
        roll = rollview.pr_roll

        # draw meterbars / notes
        roll.draw_meterbars(midi=self.midi)
        roll.draw_notes(midi=self.midi)

        # adjust y scroll
        if rollview.height < roll.height:
            rollview.scroll_y = ( (roll.height - rollview.height) / 2 ) / rollview.height
        self.parent.size = (self.parent.width, self.parent.height+1)

        # init scrollview
        rollview.update()

    # callback - scroll_x
    def _scroll_x(self, instance, scroll_x):
        pass

    # callback - buttons
    def _menu_button_play(self, instance):
        """Midi Play Button"""        
        print(instance.text,"!")
        btn = instance
        if btn.text == 'Play':
            btn.text = 'Stop'
            #self.midi.reload()
            self.midi.trigger(
                callback=self._play_callback,
                callback_timebar=self._play_callback_timebar
            )
        else:
            btn.text = 'Play'
            self.midi.stop()
            #self.now = .0     
    def _menu_button_test(self, instance):
        """Test Button"""
        pass

    # callback - midi play
    def _play_callback_timebar(self, instance, now):
        """Callback for Timebar - !!! frequent calls !!!"""
        view = self.pr_roll_view
        roll = view.pr_roll

        if now - self.now > 0.025:
            self.now = now
            
            self.bar_x = bar_x = roll.set_timebar(now)
           
            if view.local_right < bar_x:
                print('auto scroll_x before : ',view.local_right, bar_x)
                scroll_width = roll.width - view.width
                view.scroll_x = bar_x / scroll_width
                view.update_from_scroll()
                view.update()
                print('auto scroll_x after : ',view.local_right, bar_x)
            else:
                pass
                #print(view.local_right, bar_x)
    def _play_callback(self, instance, msg, now):
        '''Callback for Play'''
        pno = self.pr_piano_view.pr_piano

        # draw note_on/off status
        if msg.type == 'note_on':
            if msg.velocity == 0:
                pno.note(msg.note, on=False)
                pno.update_keyoverlay()
            else:
                pno.note(msg.note, on=True)
                pno.update_keyoverlay()
        elif msg.type == 'note_off':
            pno.note(msg.note, on=False)
            pno.update_keyoverlay()
        else:
            pass        

    # callback - piano/roll y sync
    def _roll_scroll_sync(self, instance, scroll_y):
        """Sync Scroll between piano and roll views"""
        self.pr_piano_view.scroll_y = scroll_y
    def _piano_scroll_sync(self, instance, scroll_y):
        """Sync Scroll between piano and roll views"""
        self.pr_roll_view.scroll_y = scroll_y

    # callback - keystrokes
    def _keyup(self, *args):        
        """Callback for KeyUp"""
        return True
    def _keydown(self, instance, key, keycode, text, modifiers):
        """Callback for KeyDown"""
        # zoom out
        if text == 'g':
            self.pr_roll_view.zoom_in()
        # zoom in
        elif text == 'h':
            self.pr_roll_view.zoom_out()
        # play
        elif text == ' ':
            self._menu_button_play(self.pr_menu.btn_play)
        # reload
        elif text == 'w':
            view = self.pr_roll_view
            roll = view.pr_roll
            self.midi.rewind()
            self.now=.0
            roll.set_timebar(self.now)
            view.scroll_x = 0
            view.update_from_scroll()
            view.update()
        return True

class PrApp(App):
    """Main App"""
    def build(self):
        # window size / position
        Window.size = (1024, 767)
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
        self.pr_root.pr_roll_view.show()

if __name__ == '__main__':
    PrApp().run()
