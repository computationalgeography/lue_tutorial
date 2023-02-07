#!/usr/bin/env python
import itertools
import os.path
import shlex
import subprocess
import sys

import docopt
import numpy as np

import lue.data_model as ldm


def initialize_dataset(dataset_pathname, nr_time_steps, raster_shape):
    dataset = ldm.create_dataset(dataset_pathname)

    # We assume weekly time steps
    epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, "2023-01-01", ldm.Calendar.gregorian)
    clock = ldm.Clock(epoch, ldm.Unit.week, 1)

    phenomenon_name = "planet"
    property_set_name = "surface"

    raster_view = ldm.hl.create_raster_view(
        dataset,
        phenomenon_name,
        property_set_name,
        clock,
        nr_time_steps,
        [0, nr_time_steps],
        raster_shape,
        [0, 0, *raster_shape],
    )

    property_name = "biomass"

    raster_view.add_layer("biomass", np.dtype(np.float32))

    ldm.assert_is_valid(dataset, fail_on_warning=False)

    return phenomenon_name, property_set_name, property_name


def merge_raster(dataset_pathname):
    nr_time_steps = 52
    nr_rows = 60
    nr_cols = 40
    raster_shape = (nr_rows, nr_cols)

    # 1: Initialize the dataset
    phenomenon_name, property_set_name, property_name = initialize_dataset(
        dataset_pathname, nr_time_steps, raster_shape
    )

    # 2: Spawn models and wait for them to finish writing results to the dataset
    command_lines = []
    process_id = 1

    for idxs in itertools.product(range(3), range(2)):
        hyperslab = [idx * 20 for idx in idxs] + [20, 20]
        hyperslab = "{} {} {} {}".format(*hyperslab)

        command_lines.append(
            f'./model.py {process_id} {nr_time_steps} {dataset_pathname} {phenomenon_name} {property_set_name} {property_name} "{hyperslab}"'
        )

        process_id += 1

    pipes = []

    for command_line in command_lines:
        pipes.append(subprocess.Popen(shlex.split(command_line)))

    for pipe in pipes:
        pipe.wait()

    # 3: Use the dataset containing all simulation results
    ldm.assert_is_valid(dataset_pathname, fail_on_warning=False)

    # TODO Extract slices to GeoTIFF rasters and create an animation


def main():
    usage = """\
Initialize a LUE dataset and spawn "models" that will write to it

Usage:
    {command} <dataset>

Options:
    <dataset>  Pathname of output dataset

This script first initializeѕ a single LUE dataset that will receive the
results of multiple models that are spawned afterwards.
""".format(
        command=os.path.basename(sys.argv[0])
    )

    arguments = docopt.docopt(usage)
    dataset_pathname = arguments["<dataset>"]

    merge_raster(dataset_pathname)


if __name__ == "__main__":
    sys.exit(main())
