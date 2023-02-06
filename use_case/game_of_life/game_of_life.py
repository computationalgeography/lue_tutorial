#!/usr/bin/env python
import lue.framework as lfr
import docopt
import numpy as np
import os.path
import sys


def initialize_generation(array_shape, partition_shape):

    generation = lfr.create_array(
        array_shape=array_shape,
        partition_shape=partition_shape,
        dtype=np.dtype(np.float32),
        fill_value=0,
    )

    fraction_alive_cells = 0.25
    generation = lfr.uniform(generation, 0, 1) <= fraction_alive_cells

    return generation


def save_generation(array, pathname, generation):

    lfr.to_gdal(array, "{}-{}.tif".format(pathname, generation))


def next_generation(generation):

    kernel = np.array(
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ],
        dtype=np.uint8,
    )
    nr_alive_cells = lfr.focal_sum(generation, kernel)

    # Next state of currently alive cells
    underpopulated = nr_alive_cells < 2
    overpopulated = nr_alive_cells > 3

    # Next state of currently dead cells
    reproducing = nr_alive_cells == 3

    generation = lfr.where(
        generation,
        # True if alive and not under/overpopulated
        ~(underpopulated | overpopulated),
        # True if dead with three neighbours
        reproducing,
    )

    return generation


@lfr.runtime_scope
def game_of_life(array_shape, partition_shape, nr_generations, generation_pathname):

    # The runtime is started on all localities. This function is only called on the root
    # locality.

    generation = initialize_generation(array_shape, partition_shape)
    save_generation(generation, generation_pathname, 0)

    for g in range(1, nr_generations + 1):

        generation = next_generation(generation)
        save_generation(generation, generation_pathname, g)

    # The runtime will be stopped automatically on all localities once the computations
    # are done.


usage = """\
Calculate the generations of alive cells according to the Game of Life cellular automaton

Usage:
    {command} <array_extent> <partition_extent> <nr_generations> <pathname>

Options:
    <array_extent>      Size of one side of the array
    <partition_extent>  Size of one side of the partitions
    <nr_generations>    Number of generations to calculate
    <pathname>          Pathname of GeoTiffs
""".format(
    command=os.path.basename(sys.argv[0])
)


def main():
    # Filter out arguments meant for the HPX runtime
    argv = [arg for arg in sys.argv[1:] if not arg.startswith("--hpx")]
    arguments = docopt.docopt(usage, argv)

    array_extent = int(arguments["<array_extent>"])
    assert array_extent > 0
    array_shape = 2 * (array_extent,)

    partition_extent = int(arguments["<partition_extent>"])
    assert partition_extent > 0
    partition_shape = 2 * (partition_extent,)

    assert array_extent >= partition_extent

    nr_generations = int(arguments["<nr_generations>"])
    assert nr_generations >= 0

    generation_pathname = arguments["<pathname>"]
    assert not os.path.splitext(generation_pathname)[1]

    game_of_life(array_shape, partition_shape, nr_generations, generation_pathname)


if __name__ == "__main__":
    main()
