# Copyright (c) 2017, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from __future__ import print_function
import numpy as np
from random import seed, uniform
import sys

try:
    import numpy.random_intel as rnd
    numpy_ver="Intel"
except:
    import numpy.random as rnd
    numpy_ver="regular"

try:
    from numpy import erf
    numpy_ver += "-erf"
except:
    from scipy.special import erf

try:
    from numpy import invsqrt
    numpy_ver += "-invsqrt"
except:
    #from numba import jit
    invsqrt = lambda x: 1.0/np.sqrt(x)
    #invsqrt = jit(['f8(f8)','f8[:](f8[:])'])(invsqrt)

try:
    import itimer as it
    now = it.itime
    get_mops = it.itime_mops_now
except:
    from timeit import default_timer
    now = default_timer
    get_mops = lambda t0, n: n / (1.e6 * (now() - t0))


print("Using ", numpy_ver, " numpy ", np.__version__)

######################################################
# GLOBAL DECLARATIONS THAT WILL BE USED IN ALL FILES #
######################################################

# make xrange available in python 3
try:
    xrange
except NameError:
    xrange = range

SEED = 7777777
S0L = 10.0
S0H = 50.0
XL = 10.0
XH = 50.0
TL = 1.0
TH = 2.0
RISK_FREE = 0.1
VOLATILITY = 0.2
# RISK_FREE = np.float32(0.1)
# VOLATILITY = np.float32(0.2)
# C10 = np.float32(1.)
# C05 = np.float32(.5)
# C025 = np.float32(.25)
TEST_ARRAY_LENGTH = 1024

###############################################

def gen_data(nopt):
    return (
        rnd.uniform(S0L, S0H, nopt),
        rnd.uniform(XL, XH, nopt),
        rnd.uniform(TL, TH, nopt),
        )

##############################################	

def run(name, alg, sizes=15, step=2, nopt=1024, nparr=True, dask=False, pass_args=False):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--steps', required=False, default=sizes,  help="Number of steps")
	parser.add_argument('--step',  required=False, default=step,   help="Factor for each step")
	parser.add_argument('--chunk', required=False, default=2000000,help="Chunk size for Dask")
	parser.add_argument('--size',  required=False, default=nopt,   help="Initial data size")
	parser.add_argument('--repeat',required=False, default=100,    help="Iterations inside measured region")
	parser.add_argument('--dask',  required=False, default="sq",   help="Dask scheduler: sq, mt, mp")
	parser.add_argument('--text',  required=False, default="",     help="Print with each result")
	
	args = parser.parse_args()
	sizes= int(args.steps)
	step = int(args.step)
	nopt = int(args.size)
	chunk= int(args.chunk)
	repeat=int(args.repeat)
	kwargs={}

	if(dask):
		import dask
		import dask.multiprocessing
		import dask.array as da
		dask_modes = {
		    "sq": dask.local.get_sync,
		    "mt": dask.threaded.get,
		    "mp": dask.multiprocessing.get
		}
		kwargs = {"schd": dask_modes[args.dask]}
		name += "-"+args.dask

	for i in xrange(sizes):
		price, strike, t = gen_data(nopt)
		if not nparr:
			call = [0.0 for i in range(nopt)]
			put = [-1.0 for i in range(nopt)]
			price=list(price)
			strike=list(strike)
			t=list(t)
			repeat=1 # !!!!! ignore repeat count
		if dask:
			assert(not pass_args)
			price = da.from_array(price, chunks=(chunk,), name=False)
			strike = da.from_array(strike, chunks=(chunk,), name=False)
			t = da.from_array(t, chunks=(chunk,), name=False)
		if pass_args:
			call = np.zeros(nopt, dtype=np.float64)
			put  = -np.ones(nopt, dtype=np.float64)
		iterations = xrange(repeat)
		print("ERF: {}: Size: {}".format(name, nopt), end=' ')
		sys.stdout.flush()

		if pass_args:
			alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, call, put) #warmup
			t0 = now()
			for _ in iterations:
				alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, call, put, **kwargs)
		else:
			alg(nopt, price, strike, t, RISK_FREE, VOLATILITY) #warmup
			t0 = now()
			for _ in iterations:
				alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, **kwargs)
		mops = get_mops(t0, nopt)
		print("MOPS:", mops*2*repeat, args.text)
		nopt *= step
		repeat -= step
		if repeat < 1:
		   repeat = 1
