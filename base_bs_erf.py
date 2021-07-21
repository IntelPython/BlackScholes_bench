# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


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
    from mkl_umath import erf
    numpy_ver += "-erf"
except:
    from scipy.special import erf

try:
    from mkl_umath import invsqrt
    numpy_ver += "-invsqrt"
except:
    #from numba import jit
    invsqrt = lambda x: np.true_divide(1.0, np.sqrt(x))
    #invsqrt = jit(['f8(f8)','f8[:](f8[:])'])(invsqrt)

try:
    import itimer as it
    now = it.itime
    get_mops = it.itime_mops_now
except:
    from timeit import default_timer
    now = default_timer
    get_mops = lambda t0, n: n / (1.e6 * (now() - t0))


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

def run(name, alg, sizes=15, step=2, nopt=1024, nparr=True, dask=False, mpi=False, pass_args=False):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--steps', required=False, default=sizes,  help="Number of steps")
	parser.add_argument('--step',  required=False, default=step,   help="Factor for each step")
	parser.add_argument('--chunk', required=False, default=None,   help="Chunk size for distributed computation (mutually exclusive with --chunks)")
	parser.add_argument('--chunks',required=False, default=None,   help="Number of chunks for distributed computation")
	parser.add_argument('--size',  required=False, default=nopt,   help="Initial data size")
	parser.add_argument('--repeat',required=False, default=100,    help="Iterations inside measured region")
	parser.add_argument('--dask',  required=False, default="sq",   help="Dask scheduler: sq, mt, mp or addr:port of the scheduler")
	parser.add_argument('--mpi',   required=False, default=mpi,    help="MPI scheduler")
	parser.add_argument('--text',  required=False, default="",     help="Print with each result")
	
	args = parser.parse_args()
	sizes= int(args.steps)
	step = int(args.step)
	nopt = int(args.size)
	chunks=int(args.chunks) if args.chunks else None
	chunk= int(args.chunk) if args.chunk else None
	assert(not chunks or not chunk, "Only one option can be specified: --chunk or --chunks")
	repeat=int(args.repeat)
	kwargs={}
	print("Using", numpy_ver, "numpy", np.__version__)

	if dask:
		import dask
		import dask.multiprocessing
		import dask.array as da
		dask_modes = {
		    "sq": 'synchronous',
		    "mt": 'threads',
		    "mp": 'processes'
		}
		if args.dask in dask_modes:
			kwargs = {"schd": dask_modes[args.dask]}
		else:
			import distributed
			kwargs = {"schd": distributed.Client(args.dask)}
		name += "-"+args.dask

	if args.mpi:
		from mpi4py import MPI
		comm = MPI.COMM_WORLD
		kwargs = {"comm": comm}
		mpirank = comm.Get_rank()
		assert mpirank < chunks
		nopt = nopt // chunks


	for i in xrange(sizes):

		if chunks:
			chunk = int(nopt // chunks)

		if pass_args is None:
			pass
		elif dask:
			price = da.random.uniform(S0L, S0H, nopt, chunks=(chunk,))
			strike = da.random.uniform(XL, XH, nopt, chunks=(chunk,))
			t = da.random.uniform(TL, TH, nopt, chunks=(chunk,))
		else:
			price, strike, t = rnd.uniform(S0L, S0H, nopt), rnd.uniform(XL, XH, nopt), rnd.uniform(TL, TH, nopt)

		if not nparr:
			call = [0.0 for i in range(nopt)]
			put = [-1.0 for i in range(nopt)]
			price=list(price)
			strike=list(strike)
			t=list(t)
			repeat=1 # !!!!! ignore repeat count

		if pass_args:
			call = np.zeros(nopt, dtype=np.float64)
			put  = -np.ones(nopt, dtype=np.float64)
		iterations = xrange(repeat)
		if args.mpi:
			if mpirank == 0:
				print("ERF: {}: Size: {}".format(name, nopt*chunks), end=' ')
		else:
			print("ERF: {}: Size: {}".format(name, nopt), end=' ')
		# sys.stdout.flush()

		if pass_args is None:
			alg(nopt, RISK_FREE, VOLATILITY, **kwargs) #warmup
			t0 = now()
			for _ in iterations:
				alg(nopt, RISK_FREE, VOLATILITY, **kwargs)
		elif pass_args:
			alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, call, put, **kwargs) #warmup
			t0 = now()
			for _ in iterations:
				alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, call, put, **kwargs)
		else:
			alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, **kwargs) #warmup
			t0 = now()
			for _ in iterations:
				alg(nopt, price, strike, t, RISK_FREE, VOLATILITY, **kwargs)

		if args.mpi:
			if mpirank == 0:
				mops = get_mops(t0, nopt*chunks)
				print("MOPS:", mops*2*repeat, args.text, flush=True)
		else:
				mops = get_mops(t0, nopt)
				print("MOPS:", mops*2*repeat, args.text, flush=True)

		nopt *= step
		repeat -= step
		if repeat < 1:
		   repeat = 1
