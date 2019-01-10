import sys
sys.path.append(".\\")

from kivy.config import Config
Config.set('kivy', 'kivy_clock', 'free_only')

import mido
import time

from kivy.clock import Clock
from piro.midi.clock import PrClock, PrHelper

class PrMidi():
    """ play midi file(s) with callback support """
    def __init__(self, midi_filename=None, midi_portname=None):
        """ init """
        # main members
        self.midi_file = None
        self.midi_iter = None
        self.port = None

        # play related
        self._scheduled_evt = False
        self.playing = False
        self.callback = None
        self.callback_timebar = None

        # midi file related
        self.length = None
        self.tempo = None
        self.bpm = None
        self.ppqn = None
        self.spt = None
        self.msg = None
        self.next_evt_time = 0

        # clock and helper classes
        self.clock = PrClock()
        self.helper = PrHelper()

        # actual init
        self.open(midi_filename, midi_portname)
    
    def get_tempo(self):
        """ get tempo """
        if self.midi_file:
            for msg in self.midi_file:
                if msg.is_meta and msg.type=='set_tempo':
                    return msg.tempo
        return None

    def get_ppqn(self):
        """ get ppqn(pulses per quarter note) """
        if self.tempo:
            return self.midi_file.ticks_per_beat
        return None

    def get_spt(self):
        """ get second per tick """
        if self.ppqn:
            return mido.tick2second(1, self.ppqn, self.tempo)
        return None

    def get_ticklength(self):
        """ get number of ticks for the length of the song """
        totalticks = 0
        for i, track in enumerate(self.midi_file.tracks):
            tick = 0
            for msg in track:
                tick += msg.time
            if totalticks < tick:
                totalticks = tick                
            print('track {2}: {0} ({1})'.format(track, tick, i))
        return totalticks

    def get_length(self):
        """ get total length of the song """
        return self.midi_file.length

    def open(self, midi_filename=None, midi_portname=None):
        """ open midifile and(or) port """
        if midi_filename:
            # load midi file
            self.midi_file = mido.MidiFile(midi_filename)
            # load iteration of it
            self.midi_iter = iter(self.midi_file)
            # set relative variables
            self.tempo = self.get_tempo()
            self.bpm = mido.tempo2bpm(self.tempo)
            self.ppqn = self.get_ppqn()
            self.spt = self.get_spt()
            self.next_evt_time = 0
            self.playing = False
            self.msg = None
            self.length = self.get_length()

        if midi_portname:
            self.port = mido.open_output(midi_portname)

    def reload(self):
        """ reload midi file """
        # stop if it's needed
        self.stop()

        # reload
        if self.midi_file and self.port:
            # reset port
            self.port.reset()
            # reset iteration of midi file
            del self.midi_iter
            self.midi_iter = iter(self.midi_file)
            # set relative variables
            self.tempo = self.get_tempo()
            self.bpm = mido.tempo2bpm(self.tempo)
            self.ppqn = self.get_ppqn()
            self.spt = self.get_spt()
            self.next_evt_time = 0
            self.playing = False
            self.msg = None
            self.length = self.get_length()
            self.clock.set_timer()
            # helper reset
            self.helper.reset()

    def trigger(self, msg=None, callback=None, callback_timebar=None):
        """ trigger midifile play """
        if not self.playing:
            # set flag
            self.playing = True

            try:
                self.msg = msg = next(self.midi_iter)
            except StopIteration:
                pass
            else:
                # set the next event time
                self.next_evt_time = msg.time

                # set the callback
                self.callback = callback
                self.callback_timebar = callback_timebar

                # trigger!
                self._scheduled_evt = Clock.schedule_interval_free(self.playback, self.spt)

    def play(self, msg, now=0):
        """ send one event message """
        if msg.is_meta:
            pass
            #self.helper.log(now, msg)
        else:
            self.port.send(msg)
            #self.helper.log(now, msg)

    def stop(self):
        """ stop the current playback """
        if self.playing:
            # clear flag
            self.playing = False
            # reset port
            self.port.reset()
            # unschedule the callback
            self._scheduled_evt.cancel()

    def playback(self, now=0):
        """ callback for midifile play """
        if self.playing:
            # get now
            now = self.clock.elapsed(begin_with_this=True)
            # timbar callback
            if self.callback_timebar:
                self.callback_timebar(self, now)       
            # if it's passed the next event time
            if now >= self.next_evt_time:
                # play current message
                self.play(self.msg, now)
                # run callback
                if self.callback:
                    self.callback(self, self.msg, now)
                # fetch next event message
                try:
                    self.msg = next(self.midi_iter)
                except StopIteration:
                    self.stop()
                else:
                    self.next_evt_time += self.msg.time

    def test(self):
        print(self.tempo, self.bpm, self.ppqn, self.spt)

from kivy.uix.widget import Widget
from kivy.app import App

if __name__ == '__main__':
    class PlayApp(App):
        def build(self):
            self.prMidi = prMidi = PrMidi(
                midi_filename='.\\midi\\midifiles\\fur-elise.mid',
                midi_portname='Microsoft GS Wavetable Synth 0')
    
            prMidi.test()            
            Clock.schedule_once(prMidi.trigger,0.5)

            return Widget()
    PlayApp().run()

