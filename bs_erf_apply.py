import base_bs_erf
import numpy as np
import multiprocessing
import bs_erf_naive

global bs_impl
global pool
global nump


def black_scholes(nopt, price, strike, t, rate, vol):
    global bs_impl
    global pool
    global nump
    noptpp = int(nopt/nump)
    call = np.empty(nopt, dtype=np.float64)
    put = np.empty(nopt, dtype=np.float64)
    asyncs = [pool.apply_async(bs_impl, (noptpp, price[i:i+noptpp], strike[i:i+noptpp], t[i:i+noptpp], rate, vol)) for i in range(0, nopt, noptpp)]
    for a,i in zip(asyncs, range(len(asyncs))):
        call[i:i+noptpp], put[i:i+noptpp] = a.get()
    return call, put


def main(title, impl, thepool):
    global bs_impl
    global pool
    global nump
    bs_impl = impl
    nump = multiprocessing.cpu_count()
    pool = thepool(nump)
    base_bs_erf.run(title, black_scholes, pass_args=False)
