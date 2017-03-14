DIR=$HOME/miniconda3
rm -r $DIR
mkdir -p $DIR
cd $DIR
[ -f Miniconda3-latest-Linux-x86_64.sh ] || curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $DIR -f 
#export ACCEPT_INTEL_PYTHON_EULA=yes
CONDA=$DIR/bin/conda
[ -x $CONDA ] || exit 1
$CONDA create -y -n intel3 -c intel python=3 intelpython3_core numpy numexpr scipy tbb dask numba cython mpi4py ipyparallel distarray
