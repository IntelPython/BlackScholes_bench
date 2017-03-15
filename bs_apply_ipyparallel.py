import ipyparallel
from ipyparallel import Client


class bs(object):
    def __init__(self, bs_impl):
        self.bs_impl = bs_impl

    def __call__(self, nopt, rate, vol):
        return self.bs_impl(nopt, price, strike, t, rate, vol)

        
class bs_runner(object):
    def __init__(self, bs_impl):
        self.bs_impl = bs_impl
        self.client = Client()
        self.dview = self.client[:]

    def __call__(self, nopt, price, strike, t, rate, vol):
        self.dview.scatter('price', price)
        self.dview.scatter('strike', strike)
        self.dview.scatter('t', t)
        self.dview.push(dict(call=0,put=-1))
        r = self.dview.apply(bs(self.bs_impl), t, rate, vol)
        return self.dview.gather('call').get(), self.dview.gather('put').get()
