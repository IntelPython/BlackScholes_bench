# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf
try:
    import bs_erf_cython_impl as bsc
except:
    print("Skipping Cython version. Please run 'python setup_cython_impl.py build_ext --inplace' first")
else:
    base_bs_erf.run("Cython-parallel", bsc.black_scholes_par, pass_args=True)
    base_bs_erf.run("Cython-serial", bsc.black_scholes_ser, pass_args=True)
