from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from bs_apply import bs_runner
from bs_numpy import black_scholes
import base_bs_erf

if __name__ == '__main__':
    bsr = bs_runner(black_scholes, ThreadPool(cpu_count()), cpu_count())
    base_bs_erf.run(__file__, bsr, pass_args=False)
