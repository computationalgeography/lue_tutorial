#!/usr/bin/env python
import docopt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import osgeo.gdal as gdal
import os.path
import sys


def read_raster(
        raster_pathname,
        idx):

    pathname = "{}-{}.tif".format(raster_pathname, idx)
    dataset = gdal.Open(pathname)

    return np.array(dataset.GetRasterBand(1).ReadAsArray())


def create_animation(
        raster_pathname,
        nr_rasters,
        animation_pathname):

    figure, ax = plt.subplots()
    images = []

    for i in range(nr_rasters + 1):
        im = ax.imshow(read_raster(raster_pathname, i), animated=True)

        if i == 0:
            # Show an initial one first
            ax.imshow(read_raster(raster_pathname, i))

        images.append([im])

    animation_ = animation.ArtistAnimation(figure, images, interval=50, blit=True, repeat_delay=1000)

    animation_.save(animation_pathname)


usage = """\
Create animation given a set of rasters stored in Geotiffs

Usage:
    {command} <raster> <nr_rasters> <animation>

Options:
    <raster>      Pathname of input GeoTiffs
    <nr_rasters>  Number of rasters
    <animation>   Pathname of output animation
""".format(
    command = os.path.basename(sys.argv[0]))


def main():
    arguments = docopt.docopt(usage, sys.argv[1:])

    raster_pathname = arguments["<raster>"]
    assert not os.path.splitext(raster_pathname)[1]

    nr_rasters = int(arguments["<nr_rasters>"])
    assert nr_rasters >= 0

    animation_pathname = arguments["<animation>"]

    create_animation(raster_pathname, nr_rasters, animation_pathname)


if __name__ == "__main__":
    main()
