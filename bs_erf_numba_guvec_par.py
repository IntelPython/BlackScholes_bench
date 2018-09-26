# Copyright (C) 2017 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numba as nb
from math import log, sqrt, exp, erf

def black_scholes_numba_opt(price, strike, t, mr, sig_sig_two, vol, call, put):
        P = float( price [0] )
        S = strike [0]
        T = t [0]

        a = log(P / S)
        b = T * mr[0]

        z = T * sig_sig_two[0]
        c = 0.25 * z
        y = 1./sqrt(z)

        w1 = (a - b + c) * y
        w2 = (a - b - c) * y

        d1 = 0.5 + 0.5 * erf(w1)
        d2 = 0.5 + 0.5 * erf(w2)

        Se = exp(b) * S

        res = P * d1 - Se * d2
        call [0] = res
        put [0] = res - P + Se

black_scholes_numba_opt_vec = nb.guvectorize('(f8[::1],f8[::1],f8[::1],f8[:],f8[:],f8[:],f8[::1],f8[::1])',
          '(),(),(),(),(),()->(),()', nopython=True, target="parallel", fastmath=False)(black_scholes_numba_opt)

@nb.jit
def black_scholes(nopt, price, strike, t, rate, vol, call, put):
	sig_sig_two = vol*vol*2
	mr = -rate
	black_scholes_numba_opt_vec(price, strike, t, mr, sig_sig_two, vol, call, put)

base_bs_erf.run("Numba@guvec-par", black_scholes, pass_args=True)
