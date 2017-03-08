from multiprocessing import cpu_count
from bs_threading import bs_runner
from bs_numpy import black_scholes_args
import base_bs_erf

if __name__ == '__main__':
    bsr = bs_runner(black_scholes_args, cpu_count())
    base_bs_erf.run(__file__, bsr, pass_args=True)
