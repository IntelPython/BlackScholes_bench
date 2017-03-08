from mpi4py import MPI
from bs_mpi import bs_runner
from bs_numpy import black_scholes
import base_bs_erf

if __name__ == '__main__':
    bsr = bs_runner(black_scholes)
    base_bs_erf.run(__file__, bsr, pass_args=True, verbose=MPI.COMM_WORLD.Get_rank()==0)
