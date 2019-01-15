#region environment
import sys
sys.path.append(".\\")

from kivy.config import Config
Config.set('kivy', 'kivy_clock', 'free_only')
#endregion
import mido
import time

# clocks
from kivy.clock import Clock
from piro.midi.clock import PrClock
from prio.midi.helper import PrHelper

class PrMidi():
    """ play midi file(s) with callback support """
    # init
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
        self.totalticks = None
        self.length = None
        self.tempo = None
        self.bpm = None
        self.ppqn = None
        self.spt = None
        self.msg = None
        self.next_evt_time = 0
        self.start_time = .0

        # clock and helper classes
        self.clock = PrClock()
        self.helper = PrHelper()

        # actual init
        self.open(midi_filename, midi_portname)
    
    # midifile open/reload
    def open(self, midi_filename=None, midi_portname=None):
        """ open midifile and(or) port """
        if midi_filename:
            clock = PrClock()
            clock.set_timer(1)
            # load midi file
            self.midi_file = mido.MidiFile(midi_filename)
            print("open midifile : ", clock.elapsed(1))            
            # load iteration of it
            self.midi_iter = iter(self.midi_file)
            # set relative variables
            clock.set_timer(1)
            self.tempo = self.get_tempo()
            print('get tempo : ', clock.elapsed(1))
            self.bpm = mido.tempo2bpm(self.tempo)
            self.ppqn = self.get_ppqn()
            self.spt = self.get_spt()
            self.next_evt_time = 0
            self.playing = False
            self.msg = None
            clock.set_timer(1)
            self.length = self.get_length(force=True)
            self.start_time = .0
            print('get length : ', clock.elapsed(1))

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
            self.length = self.get_length(force=True)
            self.clock.set_timer()
            self.start_time = .0
            # helper reset
            self.helper.reset()

    # get props
    def get_tempo(self):
        """ get tempo """
        if self.midi_file:
            tempotrack = self.midi_file.tracks[0]
            for msg in tempotrack:
                if msg.is_meta and msg.type=='set_tempo':
                    return msg.tempo
        return None
    def get_ppqn(self):
        """ get ppqn(pulses per quarter note) """
        if self.midi_file:
            return self.midi_file.ticks_per_beat
        return None
    def get_spt(self):
        """ get second per tick """
        if self.ppqn:
            return mido.tick2second(1, self.ppqn, self.tempo)
        return None
    def get_totalticks(self, force=False):
        """ get total ticks of the song """
        if force or not self.totalticks:
            self.get_length(force=True)
        return self.totalticks
    def get_length(self, force=False):
        """ get total length of the song """
        if force or not self.length:
            """ reset the legnth """
            tempo = 600000
            ppqn = self.ppqn
            spt = tempo / ppqn / 1000000

            totalticks = 0

            # tempo track related
            tempoticks = 0
            tempolen = .0
            lasttempo = 0
            
            tempotrack = self.midi_file.tracks[0]

            # find the total tick / length of the tempo track
            for msg in tempotrack:
                tempoticks += msg.time
                tempolen += spt * msg.time
                if msg.is_meta and msg.type == 'set_tempo':
                    if tempo != msg.tempo:
                        tempo = msg.tempo
                        spt = tempo / ppqn / 1000000
                        lasttempo = msg.tempo
            
            # find the largest ticks in the tracks
            for track in self.midi_file.tracks:
                ticks = 0
                for msg in track:
                    ticks += msg.time
                if ticks > totalticks:
                    totalticks = ticks

            # calculate and set the length
            self.length = tempolen + mido.tick2second(totalticks-tempoticks, ppqn, lasttempo)
            self.totalticks = totalticks

        return self.length
    
    # midifile trigger/play/stop
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
                self.next_evt_time += msg.time

                # set the callback
                self.callback = callback
                self.callback_timebar = callback_timebar

                # trigger!
                self._scheduled_evt = Clock.schedule_interval_free(self.playback, self.spt)
    def playback(self, now=0):
        """ callback for midifile play """
        if self.playing:
            # get now
            now = self.clock.elapsed(begin_with_this=True) + self.start_time
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
    def stop(self):
        """ stop the current playback """
        if self.playing:
            # write the start time for next trigger
            self.start_time += self.clock.elapsed(begin_with_this=True)
            print('start time :', self.start_time, self.next_evt_time)
            # clear flag
            self.playing = False
            # reset port
            self.port.reset()
            # unschedule the callback
            self._scheduled_evt.cancel()
            # clock reset
            self.clock.set_timer()
    def rewind(self):
        """ rewind to zero """
        # backup playing status
        playing = self.playing

        # stop playing temporarily
        self.playing = False
        
        # clock reset
        self.port.reset()
        self.clock.set_timer()
        self.start_time = .0
        self.next_evt_time = .0
        del self.midi_iter
        self.midi_iter = iter(self.midi_file)

        # recover playing status
        self.playing = playing
    def play(self, msg, now=0):
        """ send one event message """
        if msg.is_meta:
            pass
            #self.helper.log(now, msg)
        else:
            self.port.send(msg)
            #self.helper.log(now, msg)

if __name__ == '__main__':
    """
    from kivy.uix.widget import Widget
    from kivy.app import App
    class PlayApp(App):
        def build(self):
            self.prMidi = prMidi = PrMidi(
                midi_filename='.\\midi\\midifiles\\waldstein_1.mid',
                midi_portname='Microsoft GS Wavetable Synth 0')
    
            prMidi.test()            
            Clock.schedule_once(prMidi.trigger,0.5)

            return Widget()
    PlayApp().run()
    """
    prMidi = PrMidi(
        midi_filename='.\\midi\\midifiles\\waldstein_1.mid',
        midi_portname='Microsoft GS Wavetable Synth 0')

    clock = PrClock()

    clock.set_timer(1)
    print("length from calculation : ", prMidi.get_length(), "(", clock.elapsed(1),")")
    clock.set_timer(1)
    print("length from mido : ", prMidi.midi_file.length, "(", clock.elapsed(1), ")")