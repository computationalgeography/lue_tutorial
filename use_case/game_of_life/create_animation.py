#!/usr/bin/env python
import docopt
import imageio.v2 as iio
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import rasterio.plot
import io
import osgeo.gdal as gdal
import os.path
import sys


def slice_pathname(
        pathname,
        idx):

    return "{}-{}.tif".format(pathname, idx)


def read_raster(
        raster_pathname,
        idx):

    dataset = gdal.Open(slice_pathname(raster_pathname, idx))

    return np.array(dataset.GetRasterBand(1).ReadAsArray())


def create_animation(
        raster_pathname,
        nr_rasters,
        animation_pathname):

    figure, axis = plt.subplots()
    images = []

    for i in range(nr_rasters + 1):
        image = axis.imshow(read_raster(raster_pathname, i), animated=True)

        if i == 0:
            # Show an initial one first
            axis.imshow(read_raster(raster_pathname, i))

        images.append([image])

    animation_ = animation.ArtistAnimation(figure, images, interval=50, blit=True, repeat_delay=1000)

    animation_.save(animation_pathname)
    plt.close()


def create_animation2(
        raster_pathname,
        nr_rasters,
        animation_pathname):

    colours = [
            [216, 222, 233, 0.05],  # Dead cells: almost transparent nord4
            [191, 97, 106, 1.0],  # Alive cells: nord11
        ]
    colour_map = ListedColormap(colours)

    with iio.get_writer(animation_pathname, mode="i", fps=4) as writer:
        for i in range(nr_rasters + 1):

            figure, axis = plt.subplots(figsize=(5, 5))
            axis.set_axis_off()
            image = rasterio.plot.show(read_raster(raster_pathname, i),
                ax=axis, cmap=colour_map, vmin=0, vmax=1)

            with io.BytesIO() as buffer:
                figure.savefig(buffer, format="raw")  # , bbox_inches="tight")
                buffer.seek(0)
                data = np.frombuffer(buffer.getvalue(), dtype=np.uint8)
                nr_cols, nr_rows = figure.canvas.get_width_height()
                image = data.reshape(nr_rows, nr_cols, -1)

            writer.append_data(image)

            plt.close()


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

    create_animation2(raster_pathname, nr_rasters, animation_pathname)


if __name__ == "__main__":
    main()
