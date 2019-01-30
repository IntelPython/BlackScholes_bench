# BlackScholes benchmark
Benchmark computing Black Scholes formula using different technologies

## Prerequisites
- `icc`, if compiling native benchmarks. Intel Distribution for Python*
  2019 Gold benchmarks used icc 17.0.1.
- `mkl`, if compiling native benchmarks with MKL.

## Setup

### Linux & Mac
- Run `. activate-conda.sh` to install miniconda on Linux and Mac
- Run `make` to build and run native benchmarks
  - Run `make mkl` to build and run MKL version
  - Run `make nomkl` to build and run non-MKL version
  - Run `make black_scholes_mkl` to only build MKL version
  - Run `make black_scholes` to only build non-MKL version

### Windows
- Download & install Miniconda3 and MSYS2
- Run bash from MSYS2 and activate miniconda environment
- Run `./install-conda-envs.sh` to install Python environments


## Usage

### Native benchmarks
- Non-MKL version: Run the compiled binary `./black_scholes`.
- MKL version: Run the compiled binary `./black_scholes_mkl`.

### Python benchmarks
```
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
```

## See also
"[Accelerating Scientific Python with Intel Optimizations](http://conference.scipy.org/proceedings/scipy2017/pdfs/oleksandr_pavlyk.pdf)" by Oleksandr Pavlyk, Denis Nagorny, Andres Guzman-Ballen, Anton Malakhov, Hai Liu, Ehsan Totoni, Todd A. Anderson, Sergey Maidanov. Proceedings of the 16th Python in Science Conference (SciPy 2017), July 10 - July 16, Austin, Texas
