#!/bin/bash -x
# Copyright (C) 2017 Intel Corporation
#
# SPDX-License-Identifier: MIT

#export ACCEPT_INTEL_PYTHON_EULA=yes
DIR=$HOME/miniconda3
CONDA=$DIR/bin/conda
mkdir -p $DIR
cd $DIR
[ -x $CONDA ] || (
     [ -f Miniconda3-latest-Linux-x86_64.sh ] || curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
     bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $DIR -f 
     [ -x $CONDA ] || exit 1
)
[ -d $DIR/envs/intel3 ] || $CONDA create -y -n intel3 -c intel python=3 numpy numexpr scipy tbb dask numba cython
[ -d $DIR/envs/pip3 ] || (
     $CONDA create -y -n pip3 -c intel python=3 pip llvmlite cython
     $DIR/envs/pip3/bin/pip install numpy scipy scikit-learn toolz numexpr
     $DIR/envs/pip3/bin/pip install dask numba
)
