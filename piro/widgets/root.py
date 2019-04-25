#region environment
import sys
sys.path.append(".\\")
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
from piro.midi.helper import PrHelper
from piro.env import PrEnv

class PrRoot(BoxLayout):
    """Root Widget"""
    # init
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PrRoot, self).__init__(**kwargs)

        # props
        self.midi = PrMidi(
            midi_filename='.\\midi\\midifiles\\a-whole-new-world.mid',
            #midi_filename='.\\midi\\midifiles\\beethoven_pathetique2.mid',
            #midi_filename='.\\midi\\midifiles\\fur-elise_a tempo.mid',
            midi_portname='Microsoft GS Wavetable Synth 0')
        self.orientation = 'vertical'
        self.now = .0
        self.bar_x = .0

        # widgets add / bind
        self.widget_add()
        self.widget_bind()

        # widget shorthands
        self.pno = self.pr_piano_view.pr_piano
        self.rollview = self.pr_roll_view
        self.pianoview = self.pr_piano_view
        self.trackview = self.pr_track_view

        # bind - keystrokes
        Window.bind(on_key_up=self._keyup)
        Window.bind(on_key_down=self._keydown)        

        # draw roll
        Clock.schedule_once(self.draw_roll, 0)


    # widget factory / bind / draw
    def widget_add(self):
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
            self.pr_roll_view = widgets.PrRollView(self.midi)
            self.pr_track_view = widgets.PrTrackView(self.pr_roll_view.roll)
            self.pr_ruler_view = widgets.PrRulerView(self.pr_roll_view.roll)

        # add small widgets
        if self.pr_view:
            self.pr_view.add_widget(self.pr_piano_view)
            self.pr_view.add_widget(self.pr_roll_view)
            self.pr_view.add_widget(self.pr_track_view)
        # add big widgets
        #self.add_widget(self.pr_menu)
        self.add_widget(self.pr_view)
    def widget_bind(self):
        """
            sync y-scroll for piano / roll
            button clicks for menu
        """
        # bind - piano/roll y-sync
        self.pr_roll_view.bind(scroll_y=self._roll_scroll_sync)
        self.pr_piano_view.bind(scroll_y=self._piano_scroll_sync)

        # bind - scroll_x
        self.pr_roll_view.bind(on_scroll_start=self._scroll_start)

        # bind - buttons
        self.pr_menu.btn_play.bind(on_press=self._menu_button_play)
        self.pr_menu.btn_test.bind(on_press=self._menu_button_test)
    def draw_roll(self, instance):
        # adjust y scroll
        self.rollview.horizontal_focus()

        # adjust zoom factor
        # pipqn = self.midi.ppqn * ( roll.width / self.midi.totalticks )
        # roll.zoom_to( PrEnv.PIPQN / pipqn )

    # callback - scroll_stop
    def _scroll_start(self, instance, scroll_y):
        pass

    # callback - buttons
    def _menu_button_play(self, instance):
        """Midi Play Button"""        
        #PrHelper.msg('PrRoot', instance.text)
        btn = instance
        if btn.text == 'Play':
            btn.text = 'Stop'
            self.midi.trigger(
                callback=self._play_callback,
                callback_timebar=self._play_callback_timebar
            )
        else:
            btn.text = 'Play'
            self.midi.stop()
            self.pno.stop()
    def _menu_button_test(self, instance):
        """Test Button"""
        pass

    # callback - midi play
    def _play_callback_timebar(self, instance, now):
        """Callback for Timebar - !!! frequent calls !!!"""        
        dsec = now - self.now        
        if dsec > 0.025:
            dbar = now - self.midi.cur_evt_time
            dtick = self.midi.second2tick(dbar)            
            self.now = now
            self.rollview.focus(
                self.rollview.set_timebar(
                    itick=self.midi.cur_evt_tick + dtick
                )
            )

    def _play_callback(self, instance, msg, now):
        '''Callback for Play'''
        self.pno.play(msg)      

    # callback - piano/roll y sync
    def _roll_scroll_sync(self, instance, scroll_y):
        """Sync Scroll between piano and roll views"""
        self.pianoview.scroll_y = scroll_y
    def _piano_scroll_sync(self, instance, scroll_y):
        """Sync Scroll between piano and roll views"""
        self.rollview.scroll_y = scroll_y

    # callback - keystrokes
    def _keyup(self, *args):        
        """Callback for KeyUp"""
        return True
    def _keydown(self, instance, key, keycode, text, modifiers):
        """Callback for KeyDown"""
        view = self.rollview
        # zoom out
        if text == 'h':
            view.zoom_in()
            view.focus(view.timebar, pos='mid')
        # zoom in
        elif text == 'g':
            view.zoom_out()
            view.focus(view.timebar, pos='mid')
        # focus
        elif text == 'f':
            view.focus(view.timebar, pos='mid')
        # track
        elif text >= '0' and text <= '9':
            track = view.child.tracks.get(int(text))
            if track:
                if track.visible:
                    view.child.hide_track(int(text))
                else:
                    view.child.show_track(int(text))
            self.trackview.refresh()
        # track hide all
        elif text =='x':
            for i in view.child.tracks.tracks:
                view.child.hide_track(i)
            self.trackview.refresh()
        # track show all
        elif text == 's':
            for i in view.child.tracks.tracks:
                view.child.show_track(i)
            self.trackview.refresh()
        # play
        elif text == ' ':
            self._menu_button_play(self.pr_menu.btn_play)
        # reload
        elif text == 'w':            
            self.midi.rewind()
            self.now=.0
            view.focus(view.set_timebar(time=self.now))
        # check
        elif text == 'c':
            PrHelper.msg('PrRoot', 'scroll_y', self.pr_roll_view.scroll_y)  
        # toggle track view
        elif text == 't':
            if self.trackview.visible:
                self.pr_view.remove_widget(self.trackview)
                self.trackview.visible = False
            else:
                self.pr_view.add_widget(self.trackview)
                self.trackview.visible = True
        return True

if __name__ == '__main__':
    class PrApp(App):
        """Main App"""
        def build(self):
            # window size / position
            Window.size = (800, 600)
            Window.left, Window.top = 50, 25

            # members
            self.pr_root = PrRoot()

            # return
            return self.pr_root

    if __name__ == '__main__':
        PrApp().run()