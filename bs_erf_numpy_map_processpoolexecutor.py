from  concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from bs_executor import bs_runner
from bs_numpy import black_scholes
import base_bs_erf

if __name__ == '__main__':
    n = int(cpu_count()/2)
    with ProcessPoolExecutor(n) as executor:
        bsr = bs_runner(black_scholes, executor, n)
        base_bs_erf.run(__file__, bsr, pass_args=False)
