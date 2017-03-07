import base_bs_erf
import numpy as np
import ipyparallel
from ipyparallel import Client
import os
global client
global dview


def bs(nopt, rate, vol):
    mr = -rate
    sig_sig_two = vol * vol * 2
    
    P = price
    S = strike
    T = t
    
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
    
    return call, put


def black_scholes(nopt, price, strike, t, rate, vol): #, call, put):
    dview.scatter('price', price)
    dview.scatter('strike', strike)
    dview.scatter('t', t)
    dview.push(dict(call=0,put=-1))
    r = dview.apply(bs, t, rate, vol) #, block=False)
    return dview.gather('call').get(), dview.gather('put').get()


if __name__ == '__main__':
    global client
    global dview
    client = Client() #profile='mpi')
    dview = client[:]
    dview.execute('from numpy import log, exp')
    dview.execute('from base_bs_erf import erf, invsqrt')
    base_bs_erf.run(__file__, black_scholes, pass_args=False)
