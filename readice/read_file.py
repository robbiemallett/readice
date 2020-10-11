import struct
import numpy as np
from read_ice import get_geo_coords
from netCDF4 import Dataset

def concentration(file_location, hemisphere, with_coords=False):

    """ Reads Nasa Team sea ice concentration data.

    Reads data from the NSIDC dataset "Sea Ice Concentrations from Nimbus-7 SMMR and DMSP SSM/I-SSMIS Passive
    Microwave Data, Version 1". This data is scaled from 0 - 256 and issued on a 25x25 km polar stereographic grid.
    For more information visit https://nsidc.org/data/nsidc-0051.

    Args:
        file_location (str): location of the file to be read
        hemisphere (str): 'n' or 's', an indication of the hemisphere of the data (affects the shape of the array).
        with_coords (bool): If false, a numpy.array is returned representing the file. If True, a dictionary is
        returned with the following keys: 'data', 'lon', 'lat', 'header'. All corresponding values numpy arrays with
        the exception of 'header', which is the contents of the https://nsidc.org/data/nsidc-0051300 byte header of
        the file.

    """

    # """reads ice concentration binary file and extracts the header info and the values.
    # Then calls the function that gets the lon/lat grids and rolls all four together
    # to return a dictionary. Currently reads Nasa Team data, but nt can be changed to
    # bt (and version num changed) to read bootstrap, etc."""

    dims = get_geo_coords.get_dims(proj='ps', hemisphere=hemisphere, resolution=25)

    header_size = 300

    with open(file_location, 'rb') as fin:
        header = fin.read(header_size).decode('UTF-8')

        data = fin.read(dims[0] * dims[1])

        ints = [int(x) for x in data]

        grid = np.reshape(ints, dims).astype(float)

    if with_coords:

        geo_coords = get_geo_coords.polar_stereo(resolution=25,
                                                    hemisphere=hemisphere)

        return ({'head': header,
                 'data': grid,
                 'lon': geo_coords['lon'],
                 'lat': geo_coords['lat']})

    else:
        return(grid)


def piomas(file_location,with_coords=False):

    """ Extracts PIOMAS variables from model grid.

    Plots sea ice thickness monthly mean data from
    http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/data/model_grid. This should be extended in
    future to handle the daily mean files.

    Args:
        file_location (str): Location of file to be read.
        with_coords (bool): If false, a numpy.array is returned representing the file. If True, a dictionary is
        returned with the following keys: 'data', 'lon', 'lat', 'header'. All corresponding values numpy arrays with
        the exception of 'header', which is the contents of the https://nsidc.org/data/nsidc-0051300 byte header of
        the file.:

    Returns:
        native_data (numpy.array): 3D numpy array (first index of twelve represents months).

    """

    dims = get_geo_coords.get_dims(proj='piomas',
                                   resolution=None,
                                   hemisphere='n')

    with open(file_location, mode='rb') as file:
        fileContent = file.read()
        data = struct.unpack("f" * (len(fileContent) // 4), fileContent)

    native_data = np.full((12, dims[0], dims[1]), np.nan)

    for month in range(1, 13):
        start = (month - 1) * (dims[0] * dims[1])
        end = month * (dims[0] * dims[1])
        thickness_list = np.array(data[start:end])

        gridded = thickness_list.reshape(dims)
        native_data[month - 1, :, :] = gridded

    if with_coords:

        geo_coords = get_geo_coords.piomas_grid()

        return_dict = {'data':native_data,
                   'lon':geo_coords['lon'],
                   'lat':geo_coords['lat']}

        return(return_dict)

    else:
        return(native_data)




def SSMI_Tb(file_location, hemisphere, frequency, with_coords=False):

    """ Retrieves daily brightness temperatures on polar stereographic grid from NSIDC-0001.

    This function handles data from here: https://nsidc.org/data/NSIDC-0001/versions/5. These data should be cited as
    Meier, W. N., H. Wilcox, M. A. Hardman, and J. S. Stewart. 2019. DMSP SSM/I-SSMIS Daily Polar Gridded Brightness
    Temperatures, Version 5. [Indicate subset used]. Boulder, Colorado USA. NASA National Snow and Ice Data Center
    Distributed Active Archive Center. doi: https://doi.org/10.5067/QU2UYQ6T0B3P. [Date Accessed].

    Args:
        file_location (str): location of file to read
        hemisphere (str): 'n' or 's' to represent northern or southern hemisphere.
        frequency (float): Frequency of Tb to read (important as effects the resolution of the file).
        with_coords (bool): If True returns a dictionary that includes the geo_coordinats.

    Returns:
        data (numpy.array): 2D array of brightness temperatures, shape of which depends on grid used.

    """

    resolution = 25 if frequency < 40 else 12.5

    dims = get_geo_coords.get_dims(proj='ps', hemisphere=hemisphere, resolution=resolution)

    with open(file_location, mode='rb') as file:

        data = [int.from_bytes(file.read(2), 'little', signed=True) for i in range(dims[0] * dims[1])]

    data = np.reshape(data, dims).astype(float)/10

    geo_coords = get_geo_coords.polar_stereo(resolution=resolution,
                                                hemisphere=hemisphere)

    if with_coords:
        return_dict = {'data':data,
                       'lon':geo_coords['lon'],
                       'lat':geo_coords['lat']}


        return(return_dict)

    else:
        return(data)

def AMSR_E(file_location, freq, pol, hemisphere,
           resolution=25, with_coords=False):

    """ Processes AMSR-E/Aqua daily brightness temperatures.

    This function processes data from here: https://nsidc.org/data/ae_si25/versions/3. It should be cited as:
    Cavalieri, D. J., T. Markus, and J. C. Comiso. 2014. AMSR-E/Aqua Daily L3 25 km Brightness Temperature & Sea Ice
    Concentration Polar Grids, Version 3. [Indicate subset used]. Boulder, Colorado USA. NASA National Snow and Ice
    Data Center Distributed Active Archive Center. doi: https://doi.org/10.5067/AMSR-E/AE_SI25.003. [Date Accessed].

    Args:
        file_location (str): location of file to read
        freq (float): frequency of interest (essential for navigating the .hdf format).
        pol (str): 'v' or 'h', polarization of interest (essential for navigating the .hdf format).
        hemisphere (str): 'n' or 'h', hemisphere of the data (essential for supplying the right grid using with_coords).
        resolution (float): optional, the resolution of the grid you want supplied (if you do want one).
        with_coords (bool): optional, if True then a dictionary is supplied with the geocoordinates.

    Returns:
        data (numpy array): a 2D grid of brightness temperatures.

    """

    dataset = Dataset(file_location)

    data = np.array(dataset[f'SI_25km_{hemisphere.upper()}H_{freq}{pol.upper()}_DAY'])

    if with_coords:

        geo_coords = get_geo_coords.polar_stereo(resolution=resolution,
                                                 hemisphere=hemisphere)

        return_dict = {'data':data,
                       'lon':geo_coords['lon'],
                       'lat':geo_coords['lat']}

        return(return_dict)

    else:
        return(data)


if __name__ == '__main__':
    # pass
    from tools import plot, dict_to_nc
    import matplotlib.pyplot as plt
    import pickle
    import cartopy.crs as ccrs
    import cartopy

    #### PIOMAS Plot ####
    #
    # array = piomas('tests/test_files/heff.H1993',with_coords=True)
    #
    # plt.imshow(array['data'][0])
    # plt.show()

    # dict_to_nc(array, '../test.nc', 'SIT')
    #
    # plot(array['lon'], array['lat'], array['data'][0])

    # pickle.dump(array['data'], open('tests/test_results/piomas.p', 'wb'))


    #### AMSR Plots ####

    # Northern hemisphere 36 GHz
    #
    # array = AMSR_E('tests/test_files/AMSR_E_L3_SeaIce25km_V15_20020617.hdf',
    #                 hemisphere='n',
    #                 freq=36,
    #                 pol='V',with_coords=True)

    # dict_to_nc(array, '../test2.nc', 'SIT')
    #
    # plot(array['lon'], array['lat'], array['data'],show=True,hemisphere='n', figsize=(5,5))


    #### SSMI Plots ####

    # Northern hemisphere 37 GHz

    array = SSMI_Tb('tests/test_files/tb_f17_20190711_v5_n37h.bin',
                        'n', 37,with_coords=True)

    plot(array['lon'], array['lat'], array['data'])

    # dict_to_nc(array, '../test.nc', 'SIT')


    #####pickle.dump(array['data'], open('tests/test_results/SSMI_37_GHz_nh.p', 'wb'))

    #

    # Northern hemisphere 91 GHz
    #
    # array = SSMI_Tb('tests/test_files/tb_f17_20190727_v5_n91h.bin',
    #                     'n', 91,with_coords=True)
    #
    # plot(array['lon'], array['lat'], array['data'], hemisphere = 'n')
    #
    # pickle.dump(array['data'], open('tests/test_results/SSMI_91_GHz_nh.p', 'wb'))


    # Southern hemisphere 91 GHz

    # array = SSMI_Tb('tests/test_files/tb_f17_20190727_v5_s91h.bin',
    #                     's', 91,with_coords=True)
    #
    # #
    # plot(array['lon'], array['lat'], array['data'], hemisphere = 's', land=False)
    #
    # pickle.dump(array['data'], open('tests/test_results/SSMI_91_GHz_sh.p', 'wb'))


    # # # Southern hemisphere 19 GHz
    # #
    # array = SSMI_Tb('tests/test_files/tb_f17_20190710_v5_s19v.bin',
    #                     's', 19,with_coords=True)
    #
    # plot(array['lon'], array['lat'], array['data'], hemisphere='s')
    #
    # pickle.dump(array['data'], open('tests/test_results/SSMI_19_GHz_sh.p', 'wb'))


    # # #### Concentration Plot ####
    # #
    # # # Northern Hemisphere
    #
    # array = concentration('tests/test_files/nt_19781111_n07_v1.1_n.bin',
    #                     'n',with_coords=True)
    #
    # plot(array['lon'], array['lat'], array['data'])
    #
    # pickle.dump(array['data'], open('tests/test_results/concentration_nh.p', 'wb'))
    #
    # # # Southern Hemisphere
    #
    # array = concentration('tests/test_files/nt_19781113_n07_v1.1_s.bin',
    #                     's',with_coords=True)
    #
    # plot(array['lon'], array['lat'], array['data'], hemisphere='s')
    #
    # pickle.dump(array['data'], open('tests/test_results/concentration_sh.p', 'wb'))
