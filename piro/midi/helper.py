class PrHelper():
    def __init__(self, **kwargs):
        '''Init'''
        # reset
        self.reset()        
    def reset(self):
        '''Reset'''
        # begin of time
        self._delta_sum = 0
        self._midi_sum = 0
        self._first_call = True
        self._delta = []
    @staticmethod
    def msg_to_str(msg):
        if msg.type == 'note_on':
            return '{0:<10} | {1:<10d} | {2:<10d} | {3:<10d} | {4: 13.8f}'.format(
                'note',
                msg.channel,
                msg.note,
                msg.velocity,
                msg.time
            )                
        elif msg.type == 'control_change':
            return '{0:<10} | {1:<10d} | {2:<10d} | {3:<10d} | {4: 13.8f}'.format(
                'control',
                msg.channel,
                msg.control,
                msg.value,
                msg.time
            )
        else:
            return msg
    @staticmethod
    def msg(a, b, c=None):
        if c:
            print('[{0:10}] [{1:20}] {2}'.format(a, b, c))
        else:
            print('[{0:10}] {1}'.format(a, b))
    def log(self, elapsed, msg):
        self._midi_sum += msg.time

        if self._first_call:
            print('   elapsed    |    midi_sum   |   deviation   |   type     | channel    | note/ctrl  | vel/val    |    len       ')
            print('-----------------------------------------------------------------------------------------------------------------')
            self._first_call = False
            
        print('{0: 13.8f} | {1: 13.8f} | {2: 13.8f} | {3} '.format(
            elapsed,
            self._midi_sum,
            elapsed - self._midi_sum,
            self.msg_to_str(msg) ))        
    def msg_print(self, elapsed, delta, msg):
        self._delta_sum += delta
        self._midi_sum += msg.time
        self._delta.append(delta)
        
        if self._first_call:
            print('   elapsed    |    midi_sum   |    delta     |   deviation   | type       | channel    | note/ctrl  | vel/val    |    len       ')
            print('---------------------------------------------------------------------------------------------------------------------------------')
            self._first_call = False
            
        print('{0: 13.8f} | {1: 13.8f} | {2: 13.8f} | {3: 13.8f} | {4} '.format(
            elapsed,
            self._midi_sum,
            delta,
            delta - msg.time,
            self.msg_to_str(msg) ))

if __name__ == '__main__':
    import mido

    helper = PrHelper()
    midifile = mido.MidiFile('.\\midi\\midifiles\\fur-elise_short.mid')

    for msg in midifile:
        print(helper.msg_to_str(msg))