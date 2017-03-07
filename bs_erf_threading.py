import base_bs_erf
import numpy as np
import threading
from multiprocessing import cpu_count
import bs_erf_naive

global bs_impl
global nump


def black_scholes(nopt, price, strike, t, rate, vol, call, put):
    global bs_impl
    global nump
    noptpp = int(nopt/nump)
    threads = []
    for i in range(0, nopt, noptpp):
        thr = threading.Thread(target=bs_impl, args=(noptpp, price[i:i+noptpp], strike[i:i+noptpp], t[i:i+noptpp], rate, vol, call[i:i+noptpp], put[i:i+noptpp]))
        thr.start()
        threads.append(thr)
    for thr in threads:
        thr.join()
    return call, put


def main(title, impl):
    global bs_impl
    global nump
    bs_impl = impl
    nump = cpu_count()
    base_bs_erf.run(title, black_scholes, pass_args=True)
