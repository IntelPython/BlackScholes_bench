from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from bs_map import bs_runner
from bs_naive import black_scholes_map
import base_bs_erf

if __name__ == '__main__':
    bsr = bs_runner(black_scholes_map, ThreadPool(cpu_count()))
    base_bs_erf.run(__file__, bsr, pass_args=False)
