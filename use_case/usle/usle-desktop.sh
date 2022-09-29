#!/usr/bin/env bash
set -e


# The paths in this script correspond to the paths on Kor's development environment. Update to
# local conditions. In case the LUE Conda package is used, there is no need to set PATH and
# PYTHONPATH.
export PATH="$LUE_OBJECTS/bin:$PATH"
export PYTHONPATH="$LUE_OBJECTS/lib/python3.10:$PYTHONPATH"

# On Linux and macOS, LUE uses an alternative, faster memory allocator. It needs to be preloaded,
# before Python starts, otherwise the software will likely crash upon exit.
export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4"

data_prefix="/mnt/data1/home/kor/data/project/parallel_computing_course"
dem_pathname="$data_prefix/DGM_Tirol_10m_epsg31254_2006_2019.tif"
soil_loss_pathname="$HOME/tmp/soil_loss.tif"
partition_size=1000

python usle.py --hpx:thread=4 $partition_size $dem_pathname $soil_loss_pathname
