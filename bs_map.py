# we can put bs and bs_runner into one as soon as our driver
#  does not expect a callable but calls a member function instead
class bs(object):
    def __init__(self, bs_impl, nopt, rate, vol):
        self.nopt = nopt
        self.rate = rate
        self.vol = vol
        self.bs_impl = bs_impl

    def __call__(self, zipped):
        return self.bs_impl(self.nopt, *zipped, self.rate, self.vol)


class bs_runner(object):
    def __init__(self, bs_impl, pool):
        self.bs_impl = bs_impl
        self.pool = pool
        
    def __call__(self, nopt, price, strike, t, rate, vol):
        z = list(zip(price, strike, t))
        return self.pool.map(bs(self.bs_impl, nopt, rate, vol), z)
