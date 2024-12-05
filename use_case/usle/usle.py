#!/usr/bin/env python
import lue.framework as lfr
import docopt
import numpy as np
import os.path
import sys


def rainfall_erosivity_factor(array_shape, partition_shape):
    """
    Measure for the energy of raindrops hitting the soil and the rate of associated runoff
    """
    # For now, use the global mean value: 2190 MJ mm ha-1 h-1 yr-1
    return lfr.create_array(
        array_shape=array_shape,
        partition_shape=partition_shape,
        dtype=np.dtype(np.float32),
        fill_value=2190,
    )


def soil_erodibility_factor(array_shape, partition_shape):
    """
    Measure for the erodibility
    """
    # For now, use 0.2
    return lfr.create_array(
        array_shape=array_shape,
        partition_shape=partition_shape,
        dtype=np.dtype(np.float32),
        fill_value=0.2,
    )


def slope_length(dem, cell_size, partition_shape):
    """
    Measure for length of the slope

    High values imply high erosion rates
    """
    # Note: In case the DEM contains pits, streams won't continue from mountain tops to outlets
    # TODO fill sinks
    flow_direction = lfr.d8_flow_direction(dem)
    material = lfr.create_array(
        array_shape=dem.shape,
        partition_shape=partition_shape,
        dtype=dem.dtype,
        fill_value=1,
    )
    flow_accumulation = lfr.accu3(flow_direction, material)
    m = 0.4  # [0.2 - 0.6]

    return lfr.pow((flow_accumulation * cell_size) / 22.13, m)


def slope_gradient(dem, cell_size):
    """
    Measure for steepness of the slope

    High values imply high erosion rates
    """
    slope = lfr.slope(dem, cell_size) * 100  # Percentages
    n = 1.15  # [1.0 - 1.3]

    # TODO This results in no-data when slopes are steep
    return lfr.pow(lfr.sin(slope * 0.01745) / 0.09, n)


def topographic_factor(dem, cell_size, partition_shape):
    """
    High values imply high erosion rates
    """
    l = slope_length(dem, cell_size, partition_shape)
    s = slope_gradient(dem, cell_size)

    return (l * s) / 100


def cropping_management_factor(array_shape, partition_shape):
    """
    Measure for the effectiveness of soil and crop management systems in preventing soil loss

    Look-up of value by land cover class
    """
    # For now, just use 0.4 (shrubs)
    return lfr.create_array(
        array_shape=array_shape,
        partition_shape=partition_shape,
        dtype=np.dtype(np.float32),
        fill_value=0.4,
    )


def conservation_practices_factor(array_shape, partition_shape):
    """
    Measure for the effectiveness of practices to reduce the amount and rate of water runoff

    High values imply low erosion rates.
    """
    # For now, just use 1
    return lfr.create_array(
        array_shape=array_shape,
        partition_shape=partition_shape,
        dtype=np.dtype(np.float32),
        fill_value=1,
    )


@lfr.runtime_scope
def usle(dem_pathname, soil_loss_pathname, partition_shape):

    # The runtime is started on all localities. This function is only called on the root
    # locality.

    dem = lfr.from_gdal(dem_pathname, partition_shape=partition_shape)
    cell_size = 10

    r = rainfall_erosivity_factor(dem.shape, partition_shape)
    k = soil_erodibility_factor(dem.shape, partition_shape)
    ls = topographic_factor(dem, cell_size, partition_shape)
    c = cropping_management_factor(dem.shape, partition_shape)
    p = conservation_practices_factor(dem.shape, partition_shape)

    # Same as on Wikipedia!
    a = r * k * ls * c * p

    lfr.to_gdal(a, soil_loss_pathname, dem_pathname)

    # The runtime will be stopped automatically on all localities once the computations
    # are done.


usage = """\
Calculate the soil loss of an area using the USLE

Usage:
    {command} <nr_cells> <dem> <soil_loss>

Options:
    <nr_cells>   Size of one side of the partitions
    <dem>        Pathname of input digital elevation model
    <soil_loss>  Pathname of output soil loss raster
""".format(
    command=os.path.basename(sys.argv[0])
)


def main():
    # Filter out arguments meant for the HPX runtime
    argv = [arg for arg in sys.argv[1:] if not arg.startswith("--hpx")]
    arguments = docopt.docopt(usage, argv)

    partition_extent = int(arguments["<nr_cells>"])
    assert partition_extent > 0
    partition_shape = 2 * (partition_extent,)

    dem_pathname = arguments["<dem>"]
    soil_loss_pathname = arguments["<soil_loss>"]

    usle(dem_pathname, soil_loss_pathname, partition_shape)


if __name__ == "__main__":
    main()
