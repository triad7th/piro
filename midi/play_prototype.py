from kivy.config import Config
Config.set('kivy', 'kivy_clock', 'interrupt')

import mido
#mido.set_backend('mido.backends.pygame')

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.clock import Clock
from clock import PrClock, PrHelper
import time

class PlayApp(App):
    def build(self):        

        print(mido.get_output_names())
        self.mid = mid = mido.MidiFile('.\\source\\mido test\\midi\\beeth9-2.mid')
        self.port = mido.open_output('Pro40 MIDI 2')

        self.list_mid = list(enumerate(self.mid))
        self.tempo = self.get_tempo(self.mid)
        self.tpb = self.mid.ticks_per_beat
        self.spt = mido.tick2second(1, self.tpb, self.tempo)
        #self.spt = 0.01
        self.last_time = 0

        self.idx = 0
        self.next_event = 0 # time for the next event (in seconds)
        self.delta = 0
        self.limit = self.spt

        self.prClock = PrClock()
        self.prHelper = PrHelper()

        self.last_time = 0
        self.last_delta = 0
        self.last_msg = 0
        
        print('tempo/tps: ', self.tempo, self.spt)
        #Clock.schedule_once(self.callback, 2)
        Clock.schedule_once(self.trigger, 2)
        

        return Widget()

    def trigger(self, dt):
        self.prClock.set_timer(0)
        self.prClock.set_timer(1)
        self.next_event = self.list_mid[self.idx][1].time
        self.port.reset()
        Clock.schedule_interval(self.callback, self.spt)

    def cb(self, dt):
        print(dt- self.spt, dt, self.spt)
        
    def callback(self, dt):
        # if self.idx == 200:
        #     print (self.prHelper._delta)
        # elif self.idx > 200:
        #     return

        cur_time = self.prClock.elapsed(0, True)

        if cur_time >= self.next_event:
            msg = self.list_mid[self.idx][1]
            #print(cur_time, self.next_event, self.idx, msg)
            if not msg.is_meta:
                self.port.send(msg)
                delta = self.prClock.elapsed(1)                                
                self.prHelper.msg_print( cur_time, delta, msg )
                self.last_time = cur_time
            else:
                #self.port.send(msg)
                delta = self.prClock.elapsed(1)                                
                self.prHelper.msg_print( cur_time, delta, msg )
                self.last_time = cur_time
            self.idx += 1
            self.next_event += self.list_mid[self.idx][1].time
            self.prClock.set_timer(1)

    def callback3(self, dt):        
        cur_time = Clock.get_time()
        elapsed = 0

        while cur_time >= self.next_event and cur_time <= self.next_event + self.limit:
            msg = self.list_mid[self.idx][1]
            if not msg.is_meta:
                self.port.send(msg)
                print(cur_time, self.next_event, msg)
            self.idx += 1
            elapsed += msg.time
            cur_time += msg.time
        
        self.next_event += elapsed
        
    def get_tempo(self, midi_file):
        for msg in midi_file:
            if msg.is_meta and msg.type=='set_tempo':
                return msg.tempo
        return midi_file.DEFAULT_TEMPO

    def callback3(self, dt):
        self.idx += 1    
        self.dt += dt
        if self.idx % 0 == 0:
            print(self.idx, Clock.get_time(), time.clock())
            #print("idx/sumdt/gettime/delta/dt", self.idx, self.dt, Clock.get_time(), 0.01-dt, dt)

    def callback2(self, dt):
        self.dt = Clock.get_time() - self.dt
        print("delta/dt/get_time", 2-dt, dt, self.dt, Clock.get_time())
        self.dt = Clock.get_time()
        Clock.schedule_once(self.callback2, 2)



if __name__ == '__main__':
    PlayApp().run()