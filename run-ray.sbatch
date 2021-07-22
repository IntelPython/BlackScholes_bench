#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --nodes=64
#SBATCH --time=8:00:00
###SBATCH --cpus-per-task=30
#
set -x

OMP_NUM_THREADS=80
export OMP_NUM_THREADS
APP="python bs_erf_ray_numpy.py --repeat 1 --steps 20 --size 1024"

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
ray stop --force
srun --nodes=1 --ntasks=1 -w $node_1 --exclusive ray start --block --head --node-ip-address=$ip --port=6379 --redis-password=$redis_password --num-cpus 1 &
sleep 10

for ((  i=1; i<=$worker_num; i++ )); do
  echo "STARTING WORKER $i at ${nodes_array[$i]}";
  srun --nodes=1 --ntasks=1 -w ${nodes_array[$i]} --exclusive ray start --address $ip_head --redis-password=$redis_password --num-cpus 1
  sleep 10
  time $APP --chunks $(($i + 1)); echo "return code: $? workers: $i"
done

echo Done
scancel -f $SLURM_JOB_ID

######SBATCH --array=0-7   ### $SLURM_ARRAY_TASK_ID
#  parallel -P $SLURM_NTASKS srun  -n1 --exclusive /bin/bash -c 'echo $SLURM_ARRAY_TASK_ID $SLURM_NODEID' ::: {1..16}
