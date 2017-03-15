import numpy as np

class bs_runner(object):
    def __init__(self, bs_impl, pool, nump):
        self.bs_impl = bs_impl
        self.pool = pool
        self.nump = nump
        
    def __call__(self, nopt, price, strike, t, rate, vol):
        noptpp = int(nopt/self.nump)
        call = np.empty(nopt, dtype=np.float64)
        put = np.empty(nopt, dtype=np.float64)
        asyncs = [self.pool.apply_async(self.bs_impl, (noptpp, price[i:i+noptpp], strike[i:i+noptpp], t[i:i+noptpp], rate, vol)) for i in range(0, nopt, noptpp)]
        for a,i in zip(asyncs, range(len(asyncs))):
            call[i:i+noptpp], put[i:i+noptpp] = a.get()
        return call, put
