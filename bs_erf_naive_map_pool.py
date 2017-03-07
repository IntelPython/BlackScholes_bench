from bs_erf_map import main
from multiprocessing import Pool
from bs_erf_naive import black_scholes_map

if __name__ == '__main__':
    main(__file__, black_scholes_map, Pool)
