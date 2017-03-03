# BlackScholes benchmark
Benchmark computing Black Scholes formula using different technologies

## Setup
Use `set_python_env.sh` to install Python environment from Intel channel

## Usage
usage: {bs_erf_*.py|run.sh} [-h]
                       [--steps STEPS] [--step STEP] [--chunk CHUNK]
                       [--size SIZE] [--repeat REPEAT] [--dask DASK]
                       [--text TEXT]

optional arguments:
  -h, --help       show this help message and exit
  --steps STEPS    Number of steps
  --step STEP      Factor for each step
  --chunk CHUNK    Chunk size for Dask
  --size SIZE      Initial data size
  --repeat REPEAT  Iterations inside measured region
  --dask DASK      Dask scheduler: sq, mt, mp
  --text TEXT      Print with each result

