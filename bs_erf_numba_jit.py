import base_bs_erf
import numba as nb
from math import log, sqrt, exp, erf

@nb.jit('(i8,f8[:],f8[:],f8[:],f8,f8,f8[:],f8[:])', nopython=True, cache=True)
def black_scholes( nopt, price, strike, t, rate, vol, call, put):
    mr = -rate
    sig_sig_two = vol * vol * 2

    for i in range(nopt):
        P = float( price[i] )
        S = strike [i]
        T = t [i]

        a = log(P / S)
        b = T * mr

        z = T * sig_sig_two
        c = 0.25 * z
        y = 1./sqrt(z)

        w1 = (a - b + c) * y 
        w2 = (a - b - c) * y

        d1 = 0.5 + 0.5 * erf(w1)
        d2 = 0.5 + 0.5 * erf(w2)

        Se = exp(b) * S

        call [i] = P * d1 - Se * d2
        put [i] = call [i] - P + Se

base_bs_erf.run("Numba@jit-loop", black_scholes, nparr=True, pass_args=True)
