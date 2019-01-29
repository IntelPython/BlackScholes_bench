# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numpy as np
import dask.array as da
from numpy import log, exp
from base_bs_erf import erf, invsqrt

def black_scholes ( nopt, price, strike, t, rate, vol ):
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

	d1 = 0.5 + 0.5 * erf(w1)
	d2 = 0.5 + 0.5 * erf(w2)

	Se = exp(b) * S

	call = P * d1 - Se * d2
	put = call - P + Se

	return np.stack((call, put))

def black_scholes_dask ( nopt, price, strike, t, rate, vol, schd=None ):
	return da.map_blocks( black_scholes, nopt, price, strike, t, rate, vol, new_axis=0 ).compute(scheduler=schd)

base_bs_erf.run("Dask-agg", black_scholes_dask, dask=True)
