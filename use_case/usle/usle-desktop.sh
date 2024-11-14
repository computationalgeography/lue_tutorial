#!/usr/bin/env bash
set -e


# On Linux and macOS, LUE uses an alternative, faster memory allocator. It needs to be preloaded,
# before Python starts, otherwise the software will likely crash upon exit.
export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4"

# This example DEM is downloaded from
# https://www.data.gv.at/katalog/de/dataset/land-tirol_tirolgelnde
# DGM 10m Tirol EPSG:31254
# It is possible to use another DEM though. Note that the usle.py script currently contains a
# hard-coded cell size. Be sure to update it in case your DEM has cells of different size.
data_prefix="/mnt/data1/home/kor/data/project/parallel_computing_course"
dem_pathname="$data_prefix/DGM_Tirol_10m_epsg31254_2006_2019.tif"
soil_loss_pathname="$HOME/tmp/soil_loss.tif"

# LUE will partition the spatial domain in partitions of (partition_size, partition_size) shape.
# Small partitions result in good opportunities to hide load imbalance, at the cost of more
# overheads. Large partitions result in less opportunities to hide load imbalance, and fewer
# overheads.
partition_size=1000

# Use the number of (real) CPU cores that should be used during the calculations.
nr_threads=4
python usle.py --hpx:thread=$nr_threads $partition_size $dem_pathname $soil_loss_pathname
