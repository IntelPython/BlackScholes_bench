# Copyright (C) 2017 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
import numexpr as ne

def black_scholes ( nopt, price, strike, t, rate, vol ):
	mr = -rate
	sig_sig_two = vol * vol * 2

	P = price
	S = strike
	T = t

	a = ne.evaluate("log(P / S) ")
	b = ne.evaluate("T * mr ")

	z = ne.evaluate("T * sig_sig_two ")
	c = ne.evaluate("0.25 * z ")
	y = ne.evaluate("1/sqrt(z) ")

	w1 = ne.evaluate("(a - b + c) * y ")
	w2 = ne.evaluate("(a - b - c) * y ")

	d1 = ne.evaluate("0.5 + 0.5 * erf(w1) ")
	d2 = ne.evaluate("0.5 + 0.5 * erf(w2) ")

	Se = ne.evaluate("exp(b) * S ")

	call = ne.evaluate("P * d1 - Se * d2 ")
	put = ne.evaluate("call - P + Se ")

	return call, put

ne.set_num_threads(ne.detect_number_of_cores())
ne.set_vml_accuracy_mode('high')
base_bs_erf.run("Numexpr", black_scholes)
