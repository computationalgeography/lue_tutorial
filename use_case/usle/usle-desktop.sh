#!/usr/bin/env bash
set -e


# The paths in this script correspond to the paths on Kor's development environment. Update to
# local conditions. In case the LUE Conda package is used, there is no need to set PYTHONPATH.

# lue_translate, lue_view, ...
export PATH="$LUE_OBJECTS/bin:$PATH"

# Location of LUE Python package.
export PYTHONPATH="$LUE_OBJECTS/lib/python3.9:$PYTHONPATH"

# On Linux and macOS, LUE uses an alternative, faster memory allocator. It needs to be preloaded,
# before Python starts, otherwise the software will likely crash upon exit.
export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4"

# Perform calculations and write all results to a single dataset
python usle.py --hpx:thread=4 --partition_extent=500 /tmp/usle.lue

# Post-processing
layer_names="
    rainfall_erosivity
    soil_erodibility
    slope_length
    slope_gradient
    cropping_management
    concervation_practices
"

for layer_name in $layer_names;
do
    lue_translate export -m /tmp/usle.json /tmp/usle.lue /tmp/$layer_name.tif
done
