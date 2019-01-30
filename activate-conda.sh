#!/bin/bash -x
# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

DIR=${CONDA_PREFIX:-$HOME/miniconda3}
CONDA_PROFILE=$DIR/etc/profile.d/conda.sh
[ -f $CONDA_PROFILE ] || { # install it
    if [ `uname -s` == "Darwin" ]; then
      INST="Miniconda3-latest-MacOSX-x86_64.sh"
    elif [ `uname -s` == "Linux" ]; then
      INST="Miniconda3-latest-Linux-x86_64.sh"
    fi
    mkdir -p $DIR; cd $DIR/..
    [ -f $INST ] || curl -O https://repo.continuum.io/miniconda/$INST
    bash $INST -b -p $DIR -f
    unset INST; cd -
    [ -x $CONDA ] || exit 1
}
[ $DIR/bin/conda == `which conda` ] || { # initialize
    . $CONDA_PROFILE
}
conda activate base
[ $DIR/bin/python == `which python` ] || exit 1 # check
