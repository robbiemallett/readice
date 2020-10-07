import cartopy.crs as ccrs
import cartopy
import matplotlib.pyplot as plt
import numpy as np


def plot(lon,
              lat,
              data,
              bounding_lat=65,
              land=True,
              ocean=False,
              gridlines=True,
              figsize=None,
              save_dir=None,
              show=True,
              color_scale=(None, None),
              color_scheme='plasma',
              hemisphere='n'):
    """ Plots a 2D array of polar data with Cartopy.

    Conveniently previews data. This is useful for checking that a data array does in fact map to a set of lon/lat
    coords, or just to visualise data!

    Args:
        lon (numpy.array): a 2D array of longitude coordinates in decimal degrees East (negative for west of Greenwich, UK).
        lat (numpy.array): a 2D array of latitude coordinates in decimal degrees. Negative for values south of the equator.
        data (numpy.array): a 2D array of values to plot. Must be either the same dimensions as lon/lat arrays, or 1 smaller.
        bounding_lat (float): the minimum latitude at which values are visualised.
        land (bool): displays a land overlay when True. Default False.
        ocean (bool): displays an ocean overlay when True. Default False.
        gridlines (bool): displays gridlines when True. Default True.
        figsize (tuple): tuple of floats indicating the figure size in inches.
        save_dir (str): where specified, indicates the directory & filename where the figure should be saved.
        show: defines whether plt.show() is called, necessary for non-interactive environments.
        color_scale (tuple): tuple of floats (vmin and vmax) indicating min and max values of the colorscale
        color_scheme (str): the color mapping used by pcolormesh. Defaults to 'plasma'.
        hemisphere (str): indeicates whether northern or southern hemisphere should be plotted, 'n' or 's'.

    Returns:
        Nothing.
    """

    # Make plot
    if figsize:
        fig = plt.figure(figsize=figsize)
    else:
        fig = plt.figure()

    if hemisphere == 's':
        bounding_lat = -abs(bounding_lat)
        pole = -90
        ax = plt.axes(projection=ccrs.SouthPolarStereo())

    elif hemisphere == 'n':
        pole = 90
        ax = plt.axes(projection=ccrs.NorthPolarStereo())

    else:
        raise

    if ocean == True:
        ax.add_feature(cartopy.feature.OCEAN, zorder=2)
    if land == True:
        ax.add_feature(cartopy.feature.LAND, edgecolor='black', zorder=1)

    ax.set_extent([-180, 180, pole, bounding_lat], ccrs.PlateCarree())

    if gridlines == True:
        ax.gridlines()

    vmin, vmax = color_scale[0], color_scale[1]

    if data.shape == lat.shape:
        data = data[:-1,:-1]

    plt.pcolormesh(np.array(lon), np.array(lat), np.array(data), vmin=vmin, vmax=vmax,
                   transform=ccrs.PlateCarree(), zorder=0, cmap=color_scheme)

    plt.colorbar()

    plt.tight_layout()

    if save_dir != None:
        plt.savefig(save_dir)

    if show == True:
        plt.show()