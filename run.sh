#!/bin/bash
# Copyright (C) 2017-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT


mkdir -p logs
set -o pipefail # pass exit status of the first command in a pipe
ret=0
for i in bs_erf_*.py; do echo -e "\n$i:"; ${PYTHON:-python} $i $* | tee -a logs/$i.log || ret=1; done
exit $ret
