#!/bin/bash
# Copyright (C) 2017 Intel Corporation
#
# SPDX-License-Identifier: MIT


mkdir -p logs
for i in bs_erf_*.py; do echo -e "\n$i:"; ${PYTHON:-python} $i $* | tee -a logs/$i.log; done
