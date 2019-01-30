#!/bin/bash
# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

envs=here  # run in current environment by default
if [ -f "$CONDA_PROFILE" -o -d "$CONDA_PREFIX" ]; then        # need conda environment
    . ${CONDA_PROFILE:-$CONDA_PREFIX/etc/profile.d/conda.sh}  # initialize this bash process
    [ -x "$CONDA_PYTHON_EXE" ] || conda activate base         # activate
    # run all available environments if in base environment, otherwise run here
    [ x${CONDA_DEFAULT_ENV/base/} == x ] && envs=`ls $CONDA_PREFIX/envs`
fi
envs=${RUNENVS:-$envs} # override with external var if defined

mkdir -p logs
set -o pipefail # pass exit status of the first command in a pipe
ret=0

for e in $envs; do  # for each conda environment
    [ $e != here ] && conda activate $e   # if not here, activate
    for i in ${RUNTESTS:-bs_erf_*.py}; do echo -e "\n$i:"; ${PYTHON:-python} $i --text "$CONDA_DEFAULT_ENV" $* | tee -a logs/$i.log || ret=1; done
done
exit $ret
