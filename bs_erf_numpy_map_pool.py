from bs_erf_map import main
from multiprocessing.pool import Pool
from bs_erf_numpy import black_scholes

if __name__ == '__main__':
    main(__file__, black_scholes, Pool)
