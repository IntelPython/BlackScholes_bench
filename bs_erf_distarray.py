import distarray.globalapi as da
from distarray.globalapi import log, sqrt, exp
import numpy as np
invsqrt = lambda x: 1.0/sqrt(x)
from base_bs_erf import run, erf


def black_scholes(ctxt, nopt, price, strike, t, rate, vol):
    mr = -rate
    sig_sig_two = vol * vol * 2

    P = price
    S = strike
    T = t

    a = log(P / S)
    b = T * mr

    z = T * sig_sig_two
    c = 0.25 * z
    y = invsqrt(z)

    w1 = (a - b + c) * y
    w2 = (a - b - c) * y

    d1 = 0.5 + 0.5 * ctxt.fromarray(erf(np.asarray(w1)))
    d2 = 0.5 + 0.5 * ctxt.fromarray(erf(np.asarray(w2)))

    Se = exp(b) * S

    call = P * d1 - Se * d2
    put = call - P + Se
    
    return call, put


class bs_runner(object):
    def __init__(self, ctxt):
        self.ctxt = ctxt

    def __call__(self, nopt, price, strike, t, rate, vol):
        dprice = self.ctxt.fromarray(price)
        dstrike = self.ctxt.fromarray(strike)
        dt = self.ctxt.fromarray(t)
        ret = black_scholes(self.ctxt, nopt, dprice, dstrike, dt, rate, vol)
        return ret[0].toarray(), ret[1].toarray()


if __name__ == '__main__':
    bsr = bs_runner(da.Context())
    run(__file__, bsr, pass_args=False)
