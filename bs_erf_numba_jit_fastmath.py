# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numba as nb
from math import log, sqrt, exp, erf

@nb.njit(error_model='numpy', fastmath=True)
def black_scholes( nopt, price, strike, t, rate, vol, call, put):
    mr = -rate
    sig_sig_two = vol * vol * 2

    for i in range(nopt):
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

if __name__ == '__main__':
   base_bs_erf.run("Numba@jit-loop", black_scholes, nparr=True, pass_args=True)
