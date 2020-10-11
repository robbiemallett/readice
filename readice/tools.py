import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy
import matplotlib.pyplot as plt

def dict_to_nc(input_dict,
                output_file_destination,
                variable_name,
                attributes=None):
    """ Takes a dict with 'data', 'lon', 'lat' keys and outputs a netcdf file.

    Args:
    input_dict (dict): 'data', 'lon', 'lat' keys. 'data' value must be 2 or 3d numpy array with two dims matching those of
    'lon' and 'lat' values.
    output_file_destination (str): destination of the file and filename (e.g. ~/robbie/my_netcdf.nc)
    variable_name (str): name for the netcdf variable (e.g. 'Brightness Temperature' or 'Sea Ice Thickness').
    attributes (dict): dictionary of netcdf attributes. (e.g. {'year':2016, 'creator': 'Robbie Mallett'}

    Returns:
        0 if all runs successfully.

    """

    check_dictionary_health(input_dict)

    if len(input_dict['data'].shape) == 3:


        coords = {'lon': (['x', 'y'], input_dict['lon']),
                  'lat': (['x', 'y'], input_dict['lat']),
                  'month': (['t'], np.array(range(input_dict['data'].shape[0])))}

        variable = {f'{variable_name}': (['t', 'x', 'y'], input_dict['data'])}

    elif len(input_dict['data'].shape) == 2:

        coords = {'lon': (['x', 'y'], input_dict['lon']),
                  'lat': (['x', 'y'], input_dict['lat'])}

        variable = {f'{variable_name}': (['x', 'y'], input_dict['data'])}

    else:
        coords, variable = None, None
        raise Exception("readice currently only supports 2 & 3 dimensional arrays.")

    ds = xr.Dataset(data_vars= variable,
                    coords=coords)

    if attributes:
        for attribute in list(attributes.keys()):
            ds.attrs[attribute] = attributes[attribute]


    ds.to_netcdf(f'{output_file_destination}', 'w')

    return(0)


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

    if figsize:
        fig = plt.subplots(1,1,figsize=figsize)
    else:
        fig = plt.subplots()

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

    mesh = ax.pcolormesh(np.array(lon), np.array(lat), np.array(data),
                   vmin=vmin, vmax=vmax,
                   transform=ccrs.PlateCarree(), zorder=0,
                   cmap=color_scheme,
                   )

    plt.colorbar(mesh)

    plt.tight_layout()

    if save_dir != None:
        plt.savefig(save_dir)

    if show == True:
        plt.show()

    return(0)

def check_dictionary_health(input_dict):

    if len(input_dict['data'].shape) == 3:
        data_shape = input_dict['data'].shape
        assert data_shape[1:] == input_dict['lon'].shape
        assert input_dict['lon'].shape == input_dict['lat'].shape

    elif len(input_dict['data'].shape) == 2:

        data_shape = input_dict['data'].shape
        assert data_shape == input_dict['lon'].shape
        assert input_dict['lon'].shape == input_dict['lat'].shape
