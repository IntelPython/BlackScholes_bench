from bs_erf_apply import main
from multiprocessing.pool import ThreadPool
from bs_erf_naive import black_scholes

if __name__ == '__main__':
    main(__file__, black_scholes, ThreadPool)
