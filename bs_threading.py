import threading


class bs_runner(object):
    def __init__(self, bs_impl, nump):
        self.bs_impl = bs_impl
        self.nump = nump

    def __call__(self, nopt, price, strike, t, rate, vol, call, put):
        noptpp = int(nopt/self.nump)
        threads = []
        for i in range(0, nopt, noptpp):
            thr = threading.Thread(target=self.bs_impl, args=(noptpp, price[i:i+noptpp], strike[i:i+noptpp], t[i:i+noptpp], rate, vol, call[i:i+noptpp], put[i:i+noptpp]))
            thr.start()
            threads.append(thr)
        for thr in threads:
            thr.join()
        return call, put
