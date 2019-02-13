# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT


import numpy as np
cimport numpy as np

from cython cimport boundscheck, wraparound, cdivision, initializedcheck
from cython.parallel cimport prange, parallel
from libc.stdlib cimport srand, rand, RAND_MAX

cdef extern from "mathimf.h":
	double erf(double x) nogil
	double log(double x) nogil
	double exp(double x) nogil
	double sqrt(double x) nogil

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

# the directives below are essential for the best code generation
@boundscheck(False)
@wraparound(False)
@cdivision(True)
@initializedcheck(False)
def black_scholes_par(int nopt,
				  double[::1] price,
				  double[::1] strike,
				  double[::1] t,
				  double rate,
				  double vol,
				  double[::1] call,
				  double[::1] put):
    # using [::1] is essential for autovectorization
	cdef int i
	cdef double P, S, a, b, z, c, Se, y, T
	cdef double d1, d2, w1, w2
	cdef double mr = -rate
	cdef double sig_sig_two = vol * vol * 2

    # In order to release the GIL for a parallel loop, code in the with block cannot
    # manipulate Python objects in any way.
	with nogil, parallel():
		for i in prange(nopt):
			P = price [i]
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

@boundscheck(False)
@wraparound(False)
@cdivision(True)
@initializedcheck(False)
def black_scholes_ser(int nopt,
				  double[::1] price,
				  double[::1] strike,
				  double[::1] t,
				  double rate,
				  double vol,
				  double[::1] call,
				  double[::1] put):
    # using [::1] is essential for vectorization
	cdef int i
	cdef double P, S, a, b, z, c, Se, y, T
	cdef double d1, d2, w1, w2
	cdef double mr = -rate
	cdef double sig_sig_two = vol * vol * 2

	for i in range(nopt):
			P = price [i]
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

