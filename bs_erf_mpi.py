import base_bs_erf
import numpy as np
from mpi4py import MPI

global nump
global bs_impl


def black_scholes(nopt, price, strike, t, rate, vol, call, put):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    noptpp = int(nopt/nump)

    myprice = np.empty(noptpp, dtype=np.float64)
    mystrike = np.empty(noptpp, dtype=np.float64)
    myt = np.empty(noptpp, dtype=np.float64)

    # Scatter data into arrays
    comm.Scatter(price, myprice, root=0)
    comm.Scatter(strike, mystrike, root=0)
    comm.Scatter(t, myt, root=0)

    mycall, myput = bs_impl(noptpp, myprice, mystrike, myt, rate, vol)

    comm.Gather(mycall, call)
    comm.Gather(myput, put)

    return call, put


def main(title, impl):
    global nump
    global bs_impl
    nump = MPI.COMM_WORLD.size
    bs_impl = impl
    base_bs_erf.run(title, black_scholes, pass_args=True, verbose=MPI.COMM_WORLD.Get_rank()==0)
