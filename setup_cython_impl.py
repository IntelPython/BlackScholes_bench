# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT


from distutils.core import setup
from Cython.Build import cythonize
import os

os.environ['CC'] = "icc"
os.environ['LDSHARED'] = "icc -shared"
os.environ['CFLAGS'] = "-fimf-precision=high -qopt-report=5 -fno-alias -xhost -qopenmp -pthread -fno-strict-aliasing"

setup(
    name = "bs_erf_cython_impl",
    ext_modules = cythonize("bs_erf_cython_impl.pyx"),
)
