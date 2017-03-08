import numpy as np
from mpi4py import MPI

class bs_runner(object):
    def __init__(self, bs_impl):
        self.bs_impl = bs_impl
        self.nump = MPI.COMM_WORLD.size

    def __call__(self, nopt, price, strike, t, rate, vol, call, put):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        noptpp = int(nopt/self.nump)
        
        myprice = np.empty(noptpp, dtype=np.float64)
        mystrike = np.empty(noptpp, dtype=np.float64)
        myt = np.empty(noptpp, dtype=np.float64)
        
        # Scatter data into arrays
        comm.Scatter(price, myprice, root=0)
        comm.Scatter(strike, mystrike, root=0)
        comm.Scatter(t, myt, root=0)
        
        mycall, myput = self.bs_impl(noptpp, myprice, mystrike, myt, rate, vol)
        
        comm.Gather(mycall, call)
        comm.Gather(myput, put)
        
        return call, put
