import base_bs_erf
import multiprocessing

global bs_impl
global pool
global nump


class bs(object):
    def __init__(self, nopt, rate, vol):
        self.nopt = nopt
        self.rate = rate
        self.vol = vol

    def __call__(self, zipped):
        return bs_impl(self.nopt, *zipped, self.rate, self.vol)


def black_scholes(nopt, price, strike, t, rate, vol):
    global bs_impl
    global pool
    z = list(zip(price, strike, t))
    return pool.map(bs(nopt, rate, vol), z)


def main(title, impl, thepool):
    global bs_impl
    global pool
    global nump
    bs_impl = impl
    nump = multiprocessing.cpu_count()
    pool = thepool(nump)
    base_bs_erf.run(title, black_scholes, pass_args=False)
