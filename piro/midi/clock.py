import time

class PrClock():
    def __init__(self, **kwargs):
        '''Init'''
        # begin of time
        self._begin = [0, time.time()]
        # first elapsed
        self._first = [True, True]
    def set_timer(self, n=0):
        if n == 0:
            self._begin[n] = time.time()
            self._first[n] = True
            return self._begin[n]
        elif n > 0 and len(self._begin) > n:
            self._begin[n] = time.time()
            self._first[n] = True
            return self._begin[n]
        return self._begin[0]
    def add_timer(self):
        self._begin.append(time.time())   
        self._first.append(True)      
    def elapsed(self, n=0, begin_with_this=False):
        # current time
        cur_time = time.time()

        # if begin_with_this is true, reset the clock and start with zero delay
        if begin_with_this and self._first[n]:
            self._first[n] = False
            self._begin[n] = cur_time

        return cur_time - self._begin[n]

if __name__ == '__main__':
    import random
    clock = PrClock()
    print('million times integer multiply')
    clock.set_timer()
    for i in range(1000000):
        x = random.randint(1, 1000) * random.randint(1, 1000)
    print(clock.elapsed(),'sec elapsed.')
