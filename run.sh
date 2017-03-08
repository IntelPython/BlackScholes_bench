#!/bin/bash

mkdir -p logs
for i in `ls bs_erf_*.py | egrep -v '_mpi|_ipyparallel'`; do
    echo -e "\n$i:"
    ${PYTHON:-python} $i $* | tee -a logs/$i.log
done
for i in `ls bs_erf_*.py | grep _mpi`; do
    echo -e "\n$i:"
    mpirun -n 16 ${PYTHON:-python} $i $* | tee -a logs/$i.log;
done
ipcluster start -n 16 --daemonize=True
sleep 5; sync
for i in `ls bs_erf_*.py | grep _ipyparallel`; do
    echo -e "\n$i:"
    ${PYTHON:-python} $i $* | tee -a logs/$i.log
done
ipcluster stop
