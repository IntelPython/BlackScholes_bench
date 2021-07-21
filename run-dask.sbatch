#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --nodes=64
#SBATCH --time=4:00:00
#
set -x
rm $HOME/global/dask.sch
OMP_NUM_THREADS=80
export OMP_NUM_THREADS
APP="python bs_erf_dask_map_numpy.py --dask `hostname -i`:41041 --repeat 1 --steps 20 --size 1000"

redis_password="5241590000000000"  #$(uuidgen)
export redis_password

echo "$SLURM_JOB_NUM_NODES nodes from `hostname`"
worker_num=$(($SLURM_JOB_NUM_NODES - 1)) #number of nodes other than the head node
nodes=$(scontrol show hostnames $SLURM_JOB_NODELIST) # Getting the node names
nodes_array=( $nodes )

node_1=${nodes_array[0]}
ip=$(srun --nodes=1 --ntasks=1 -w $node_1 hostname --ip-address) # making redis-address
port=6379
ip_head=$ip:$port
export ip_head
echo "IP Head: $ip_head"

echo "STARTING HEAD at $node_1"
rm -f /home/amalakho/global/dask.sch
srun --nodes=1 --ntasks=1 -w $node_1 --exclusive dask-scheduler --interface eth0 --port 41041 --scheduler-file $HOME/global/dask.sch &
sleep 10


for ((  i=1; i<=$worker_num; i++ )); do
  echo "STARTING WORKER $i at ${nodes_array[$i]}";
  srun --nodes=1 --ntasks=1 -w ${nodes_array[$i]} --exclusive /bin/bash -xc 'dask-worker --scheduler-file $HOME/global/dask.sch' &
  sleep 10
  time $APP --chunks 64; echo "return code: $? workers: $i"
done

echo Done
killall dask-scheduler
scancel -f $SLURM_JOB_ID

######SBATCH --array=0-7   ### $SLURM_ARRAY_TASK_ID
#  parallel -P $SLURM_NTASKS srun  -n1 --exclusive /bin/bash -c 'echo $SLURM_ARRAY_TASK_ID $SLURM_NODEID' ::: {1..16}
