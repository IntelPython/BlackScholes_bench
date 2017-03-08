from multiprocessing import Pool
from multiprocessing import cpu_count
from bs_map import bs_runner
from bs_numpy import black_scholes
import base_bs_erf

if __name__ == '__main__':
    n = int(cpu_count()/2)
    bsr = bs_runner(black_scholes, Pool(n))
    base_bs_erf.run(__file__, bsr, pass_args=False)
