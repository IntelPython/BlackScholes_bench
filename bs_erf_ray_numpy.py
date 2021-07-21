# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numpy as np
from numpy import log, exp
from base_bs_erf import rnd, erf, invsqrt, S0L, S0H, XL, XH, TL, TH
import ray

ray.init(address='auto', _redis_password='5241590000000000')

@ray.remote
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

	return sum(np.stack((call, put)))


def black_scholes_ray(nopt, rate, vol):
	futures = [black_scholes.remote(nopt//64, rate, vol) for _ in range(64)]
	ray.get(futures)

if __name__ == '__main__':
	base_bs_erf.run("Ray-numpy", black_scholes_ray, pass_args=None)
