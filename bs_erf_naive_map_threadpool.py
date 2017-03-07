from bs_erf_map import main
from multiprocessing.pool import ThreadPool
from bs_erf_naive import black_scholes_map

if __name__ == '__main__':
    main(__file__, black_scholes_map, ThreadPool)
