#!/usr/bin/env bash
set -e


# On Linux and macOS, LUE uses an alternative, faster memory allocator. It needs to be preloaded,
# before Python starts, otherwise the software will likely crash upon exit.
export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4"

# Adjust these to your liking and the capabilities of your hardware
# When using large arrays, the size of the generated animated gif should be enlarged. Otherwise
# the alive cells won't be visible. See create_animation.py.
nr_threads=4
array_size=10000
partition_size=1000
nr_generations=100
generation_pathname="$HOME/tmp/generation"
animation_pathname="$HOME/tmp/game_of_life.gif"

echo "Perform calculations ..."
python game_of_life.py --hpx:thread=$nr_threads \
    $array_size $partition_size $nr_generations $generation_pathname
echo "... done"
echo "Create animation ..."
python create_animation.py $generation_pathname $nr_generations $animation_pathname
mogrify -trim +repage $animation_pathname
echo "... done"
