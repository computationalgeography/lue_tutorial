#!/usr/bin/env python
import os
import sys
import time

import docopt
import numpy as np

import lue.data_model as ldm


def run_model(
    process_id,
    nr_time_steps,
    dataset_pathname,
    phenomenon_name,
    property_set_name,
    property_name,
    hyperslab,
):

    row, col, nr_rows, nr_cols = hyperslab
    raster_shape = (nr_rows, nr_cols)

    object_id = 5
    time_box_idx = 0

    # "Run model"
    for t in range(nr_time_steps):

        # Simulate current time step
        biomass = np.full(
            shape=(1, *raster_shape),
            dtype=np.float32,
            fill_value=(100 * process_id) + t,
        )

        # Open dataset and write results
        data_written = False

        # Another process might be busy writing its data. If so, keep trying.
        while not data_written:
            try:
                dataset = ldm.open_dataset(dataset_pathname, "w")
                property_ = (
                    dataset.phenomena[phenomenon_name]
                    .property_sets[property_set_name]
                    .properties[property_name]
                )
                property_.value[object_id][
                    time_box_idx, t, row : row + nr_rows, col : col + nr_cols
                ] = biomass
                data_written = True
            except RuntimeError as exception:
                if "Cannot write to" in str(exception):
                    raise
                time.sleep(1)


def main():
    usage = """\
Run a simulation model and write results to an existing dataset

Usage:
    {command} <process> <time_steps>
        <dataset> <phenomenon> <property_set> <property> <hyperslab>

Options:
    <process>       ID of the process. Use to write unique values per process.
    <time_steps>    Number of time steps to write
    <dataset>       Pathname to existing dataset to write to
    <phenomenon>    Name of phenomenon containing property-set
    <property_set>  Name of property-set containing property
    <property>      Name of property to write spatio-temporal raster cells to
    <hyperslab>     Definition of subset into existing LUE value to write
                    result to.

It is assumed here that the dataset already exists and contains a LUE value
to which spatio-temporal gridded data can be written to. This value must be
located at the path phenomenon/property-set/property passed in.
""".format(
        command=os.path.basename(sys.argv[0])
    )

    arguments = docopt.docopt(usage)
    process_id = int(arguments["<process>"])
    nr_time_steps = int(arguments["<time_steps>"])
    dataset_pathname = arguments["<dataset>"]
    phenomenon_name = arguments["<phenomenon>"]
    property_set_name = arguments["<property_set>"]
    property_name = arguments["<property>"]
    hyperslab = [int(v) for v in arguments["<hyperslab>"].split()]

    run_model(
        process_id,
        nr_time_steps,
        dataset_pathname,
        phenomenon_name,
        property_set_name,
        property_name,
        hyperslab,
    )


if __name__ == "__main__":
    sys.exit(main())
