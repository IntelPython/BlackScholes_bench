# we can put bs and bs_runner into one as soon as our driver
#  does not expect a callable but calls a member function instead
class bs(object):
    def __init__(self, bs_impl, nopt, rate, vol):
        self.nopt = nopt
        self.rate = rate
        self.vol = vol
        self.bs_impl = bs_impl

    def __call__(self, *iterables):
        return self.bs_impl(self.nopt, *iterables, self.rate, self.vol)


class bs_runner(object):
    def __init__(self, bs_impl, executor, nump):
        self.bs_impl = bs_impl
        self.executor = executor
        self.nump = nump
        
    def __call__(self, nopt, price, strike, t, rate, vol):
        return self.executor.map(bs(self.bs_impl, nopt, rate, vol), price, strike, t, chunksize=int(nopt/self.nump))
