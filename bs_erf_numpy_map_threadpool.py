from bs_erf_map import main
from multiprocessing.pool import ThreadPool
from bs_erf_numpy import black_scholes

if __name__ == '__main__':
    main(__file__, black_scholes, ThreadPool)
