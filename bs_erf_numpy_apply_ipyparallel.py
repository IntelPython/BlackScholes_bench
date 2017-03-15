from bs_apply_ipyparallel import bs_runner
from bs_numpy import black_scholes
import base_bs_erf

if __name__ == '__main__':
    bsr = bs_runner(black_scholes)
    base_bs_erf.run(__file__, bsr, pass_args=False)
