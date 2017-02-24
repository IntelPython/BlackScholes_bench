#!/bin/bash

mkdir -p logs
for i in bs_erf_*.py; do echo -e "\n$i:"; ${PYTHON:-python} $i $* | tee -a logs/$i.log; done
