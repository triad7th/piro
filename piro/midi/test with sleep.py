import mido
import time
from clock import PrClock, PrHelper

print(mido.get_output_names())
mid = mido.MidiFile('.\\source\\mido test\\midi\\beeth9-2.mid')


# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

port = mido.open_output('Microsoft GS Wavetable Synth 0')


# for msg in mid.play():
#     print(msg)
#     port.send(msg)


for msg in mid:
    if msg.is_meta and msg.type=='set_tempo':
        print("tempo is :",msg.tempo)
        break

prClock = PrClock()
prHelper = PrHelper()
for msg in mid:
    prClock.set_timer(0)
    prClock.set_timer(1)
    time.sleep(msg.time)
    delta = prClock.elapsed(1)
    if not msg.is_meta:
        prHelper.msg_print(prClock.elapsed(0), prClock.elapsed(1), msg)
        port.send(msg)
