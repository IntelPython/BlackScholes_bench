# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import dask.array as da
from dask.array import log, sqrt, exp
from base_bs_erf import erf, invsqrt

def black_scholes ( nopt, price, strike, t, rate, vol, schd=None):
	mr = -rate
	sig_sig_two = vol * vol * 2

	P = price
	S = strike
	T = t

	a = log(P / S)
	b = T * mr

	z = T * sig_sig_two
	c = 0.25 * z
	y = da.map_blocks(invsqrt, z)

	w1 = (a - b + c) * y
	w2 = (a - b - c) * y

	d1 = 0.5 + 0.5 * da.map_blocks(erf, w1)
	d2 = 0.5 + 0.5 * da.map_blocks(erf, w2)

	Se = exp(b) * S

	call = P * d1 - Se * d2
	put = call - P + Se

	return da.compute( da.stack((put, call)), scheduler=schd )

base_bs_erf.run("Dask", black_scholes, dask=True)
