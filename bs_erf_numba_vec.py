# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numba as nb
from math import log, sqrt, exp, erf

def black_scholes_numba_opt(price, strike, t, mr, sig_sig_two):
        P = price
        S = strike
        T = t

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
        return complex(r, r - P + Se)

black_scholes_numba_opt_vec = nb.vectorize(nopython=True, fastmath=True)(black_scholes_numba_opt)

@nb.njit
def black_scholes(nopt, price, strike, t, rate, vol):
    sig_sig_two = vol*vol*2
    mr = -rate
    black_scholes_numba_opt_vec(price, strike, t, mr, sig_sig_two)

if __name__ == '__main__':
    base_bs_erf.run("Numba@vec-par", black_scholes, pass_args=False)
