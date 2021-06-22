# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numpy as np
import dask
import dask.array as da
from numpy import log, exp
from base_bs_erf import rnd, erf, invsqrt, S0L, S0H, XL, XH, TL, TH

def black_scholes ( nopt, rate, vol ):
	mr = -rate
	sig_sig_two = vol * vol * 2

	P, S, T = rnd.uniform(S0L, S0H, nopt), rnd.uniform(XL, XH, nopt), rnd.uniform(TL, TH, nopt)

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

def black_scholes_dask ( nopt, rate, vol, schd=None ):
	res = schd.map( lambda x: black_scholes(nopt//64, rate, vol), range(64) )
	return schd.submit(sum, res).result()
	#return schd.gather(res)


if __name__ == '__main__':
	base_bs_erf.run("Dask-map-agg", black_scholes_dask, dask=True, pass_args=None)
