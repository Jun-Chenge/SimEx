#! /bin/bash

# Sample installation script. Adjustments might be neccessary.

#HOSTNAME=`hostname`
#if [[ "$HOSTNAME" == max-*.desy.de ]]
#then
    #THIRD_PARTY_ROOT=/data/netapp/s2e/simex
    #git apply patch_for_maxwell
#else
    #THIRD_PARTY_ROOT=
#fi

echo $THIRD_PARTY_ROOT

MODE=$1
if [ $MODE = "maxwell" ]
then
    echo $MODE
    INSTALL_PREFIX=$THIRD_PARTY_ROOT
    DEVELOPER_MODE=OFF
    XCSIT=OFF
elif [ $MODE = "develop" ]
then
    echo $MODE
    INSTALL_PREFIX=..
    DEVELOPER_MODE=ON
    XCSIT=ON
fi


# Build for python3.4

# Check for existing build directory, remove if found
if [ -d build ]
then
    echo "Found build/ directory, will remove it now."
    rm -rvf build
fi

# Create new build dir and cd into it.
mkdir -v build
cd build
echo "Changed dir to $PWD."

# Uncomment the next line if you want to use Intel Fotran compiler
# (otherwise gfortran will be used). Make sure $MKLROOT is set. This can be achieved by
# $> source `which compilervars.sh` <arch>
# where <arch> is either intel64 or ia32
export FC=ifort

THIRD_PARTY_ROOT=/data/netapp/s2e/simex
INSTALL_PREFIX=$HOME/py3.7
# Some needed environment variables.
export BOOST_ROOT=${THIRD_PARTY_ROOT}
export Boost_NO_SYSTEM_PATHS=ON
export XERCESC_ROOT=${THIRD_PARTY_ROOT}
export GEANT4_ROOT=${THIRD_PARTY_ROOT}
export Geant4_DIR=${THIRD_PARTY_ROOT}/lib64/Geant4-10.4.0
export XCSIT_ROOT=${THIRD_PARTY_ROOT}

cmake -DSRW_OPTIMIZED=ON \
      -DDEVELOPER_INSTALL=$DEVELOPER_MODE \
      -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX \
      -DUSE_SingFELPhotonDiffractor=ON \
      -DUSE_CrystFELPhotonDiffractor=ON \
      -DUSE_GAPDPhotonDiffractor=ON \
      -DUSE_s2e=ON \
      -DUSE_S2EReconstruction_EMC=ON \
      -DUSE_S2EReconstruction_DM=ON \
      -DUSE_wpg=ON \
      -DUSE_GenesisPhotonSource=ON \
      -DUSE_XCSITPhotonDetector=$XCSIT \
      -DUSE_FEFFPhotonInteractor=ON \
      -DXERCESC_ROOT=$XERCESC_ROOT \
      -DGEANT4_ROOT=$GEANT4_ROOT \
      -DXCSIT_ROOT=$XCSIT_ROOT \
      -DBOOST_ROOT=$BOOST_ROOT \
      ..

# Build the project.
make -j32

# Install the project.
make install

cd ..

# Revert
git checkout -- CMakeLists.txt
