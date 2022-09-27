#!/usr/bin/env python
import lue.data_model as ldm
import lue.framework as lfr
import docopt
import numpy as np
import json
import os.path
import sys


def rainfall_erosivity_factor(
        partition_shape):

    array_shape = (3000, 3000)
    result = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=1.1)
    print(lfr.minimum(result).get())

    return result


def soil_erodibility_factor(
        partition_shape):

    array_shape = (3000, 3000)
    result = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=2.2)

    return result


def slope_length(
        partition_shape):

    array_shape = (3000, 3000)
    result = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=3.3)

    return result


def slope_gradient(
        partition_shape):

    array_shape = (3000, 3000)
    result = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=4.4)

    return result


def cropping_management_factor(
        partition_shape):

    array_shape = (3000, 3000)
    result = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=5.5)

    return result


def concervation_practices_factor(
        partition_shape):

    array_shape = (3000, 3000)
    result = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=6.6)

    return result


def write_translate_json(
        dataset_pathname,
        phenomenon_name,
        property_set_name,
        layer_names):
    """
    Create the file that lue_translate currently needs for exporting
    an array from a LUE dataset to a GDAL raster
    """
    dataset_directory_pathname, dataset_basename = os.path.split(dataset_pathname)
    dataset_basename = os.path.splitext(dataset_basename)[0]

    object_ = {
        dataset_basename: {
            "phenomena": [
                {
                    "name": phenomenon_name,
                    "property_sets": [
                        {
                            "name": property_set_name,
                            "properties": [
                                { "name": layer_name for layer_name in layer_names}
                             ]
                        }
                    ]
                }
            ]
        }
    }

    meta_pathname = os.path.join(dataset_directory_pathname, dataset_basename + ".json")

    open(meta_pathname, "w", encoding="utf8").write(json.dumps(object_, indent=4))


def write_usle_results(
        io_tuples,
        dataset_pathname):

    phenomenon_name = "area"
    property_set_name = "area"
    array_shape = io_tuples[0][0].shape
    space_box = [0, 0, *array_shape]

    dataset = ldm.create_dataset(dataset_pathname)
    raster_view = ldm.hl.create_raster_view(
        dataset, phenomenon_name, property_set_name, array_shape, space_box)

    for array, layer_name in io_tuples:
        raster_view.add_layer(layer_name, array.dtype)
        array_pathname = "{}/{}/{}/{}".format(
            dataset_pathname, phenomenon_name, property_set_name, layer_name)
        lfr.write_array(array, array_pathname)

    write_translate_json(
        dataset_pathname, phenomenon_name, property_set_name, [layer_name for _, layer_name in io_tuples])


@lfr.runtime_scope
def usle(
        partition_shape,
        dataset_pathname):

    # The HPX runtime is started on all localities. This function is only called on the root
    # locality.

    r = rainfall_erosivity_factor(partition_shape)
    k = soil_erodibility_factor(partition_shape)
    l = slope_length(partition_shape)
    s = slope_gradient(partition_shape)
    c = cropping_management_factor(partition_shape)
    p = concervation_practices_factor(partition_shape)

    a = r * k * l * s * c * p

    io_tuples = [
        (r, "rainfall_erosivity"),
        (k, "soil_erodibility"),
        (l, "slope_length"),
        (s, "slope_gradient"),
        (c, "cropping_management"),
        (p, "concervation_practices"),
        (a, "erosivity"),
    ]
    write_usle_results(io_tuples, dataset_pathname)

    # The HPX runtime will be stopped automatically on all localities once the computations
    # are done.


usage = """\
Calculate the soil loss of an area using the USLE

Usage:
    {command} --partition_extent=<nr_cells> <dataset>

Options:
    partition_extent=<nr_cells>  Size of one side of the partitions: nr_cells
    <dataset>                    Pathname of dataset to write result to
""".format(
    command = os.path.basename(sys.argv[0]))


# def parse_tuple(string):
# 
#     return tuple([token.strip() for token in string.split(",")])
# 
# 
# def parse_shape(string):
# 
#     return tuple([int(element) for element in parse_tuple(string)])


def main():
    # Filter out arguments meant for the HPX runtime
    argv = [arg for arg in sys.argv[1:] if not arg.startswith("--hpx")]
    arguments = docopt.docopt(usage, argv)

    partition_extent = int(arguments["--partition_extent"])
    assert partition_extent > 0
    partition_shape = 2 * (partition_extent,)

    dataset_pathname = arguments["<dataset>"]

    usle(partition_shape, dataset_pathname)


if __name__ == "__main__":
    main()
