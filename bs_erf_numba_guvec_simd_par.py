# Copyright (C) 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numba as nb
from math import log, sqrt, exp, erf

@nb.njit('(f8[::1],f8[::1],f8[::1],f8,f8,f8[::1],f8[::1])', error_model='numpy', fastmath=True)
def black_scholes_jit( price, strike, t, mr, sig_sig_two, call, put):
    for i in range(price.size):
        P = price[i]
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

        r  = P * d1 - Se * d2
        call [i] = r
        put [i] = r - P + Se

@nb.guvectorize('(f8[::1],f8[::1],f8[::1],f8[:],f8[:],f8[::1],f8[::1])',
    '(a),(a),(a),(),()->(a),(a)', nopython=True, target="parallel")
def black_scholes_numba_vec(price, strike, t, mr, sig_sig_two, call, put):
    black_scholes_jit( price, strike, t, mr[0], sig_sig_two[0], call, put)

@nb.jit
def black_scholes(nopt, price, strike, t, rate, vol, call, put):
    sig_sig_two = vol*vol*2
    mr = -rate
    black_scholes_numba_vec(price.reshape((-1,512)), strike.reshape((-1,512)), t.reshape((-1,512)),
                                mr, sig_sig_two, call.reshape((-1,512)), put.reshape((-1,512)).reshape((-1,512)))

base_bs_erf.run("Numba@guvec-par-simd", black_scholes, pass_args=True)
