#!/bin/bash -x
# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

# Input arguments
pyvers=${PYVERS:-3}                                         # Python versions to install, 3 is default
channels=${CHANNELS:-intel defaults pip}                    # channels to intall from
# list of packages to install
pkgs=${PACKAGES:-numpy numexpr scipy dask numba cython toolz cloudpickle}

. ${CONDA_PROFILE:-$CONDA_PREFIX/etc/profile.d/conda.sh}  # initialize this bash process
conda activate base
[ -x "$CONDA_EXE" -a -d "$CONDA_PREFIX" ] || exit 1       # Sanity check

conda_install () {
    n=$1; shift
    $CONDA_EXE `[ -d $CONDA_PREFIX/envs/$n ] && echo install || echo create` -y -n $n -m $*
}
# Update conda package
$CONDA_EXE update -n base -c defaults -y conda

# For all channels, all python versions, install all packages
for v in $pyvers; do
    for c in $channels; do
        if [ x$c == xpip ]; then
            conda_install pip$v python=$v pip
            conda activate pip$v
            pip install -U --isolated $pkgs
            conda activate base
        else
            conda_install $c$v -c $c python=$v $pkgs
        fi
    done
done
