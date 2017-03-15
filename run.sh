#!/bin/bash

export MKL_NUM_THREADS=1

mkdir -p logs
for i in `ls bs_erf_*.py | egrep -v '_mpi|_ipyparallel|pool'`; do
    echo -e "\n$i:"
    ${PYTHON:-python} $i $* | tee -a logs/$i.log
done
for i in `ls bs_erf_*.py | grep _mpi`; do
    echo -e "\n$i:"
    mpirun -genv I_MPI_SHM_LMT=shm -n 16 ${PYTHON:-python} $i $* | tee -a logs/$i.log;
done
ipcluster start -n 16 --daemonize=True
sync; sleep 20; sync
for i in `ls bs_erf_*.py | grep _ipyparallel`; do
    echo -e "\n$i:"
    ${PYTHON:-python} $i $* | tee -a logs/$i.log
done
ipcluster stop
for i in `ls bs_erf_*pool*.py`; do
    echo -e "\n$i:"
    ${PYTHON:-python} $i $* | tee -a logs/$i.log
done
