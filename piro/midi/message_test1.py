import mido
import time

port = mido.open_output('Pro40 MIDI 2')
port.send(mido.Message('note_on', note=60, velocity=120, time=1.0))
time.sleep(2)
port.send(mido.Message('note_on', note=60, velocity=0, time=1.0))
port.send(mido.Message('note_on', note=62, velocity=120, time=1.0))
time.sleep(2)