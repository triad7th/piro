import time

class PrClock():
    def __init__(self, **kwargs):
        # begin of time
        self._begin = [0, time.time()]
        # first elapsed
        self._first = [True, True]
    def set_timer(self, n=0):
        """ initialize the n-th timer """
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
        """ add the timer """
        self._begin.append(time.time())   
        self._first.append(True)      
    def count_timer(self):
        """ return the total number of counters """
        return len(self._begin)
    def elapsed(self, n=0, begin_with_this=False):
        """ return the elapsed time for n-th timer
        begin_with_this = the first call of this will be 0 elapsed time
        """
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
