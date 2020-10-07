import struct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_dims(proj, resolution, hemisphere):

    if 'pio' in proj.lower():
        dims = (360, 120)

    elif (proj == 'ps') & (resolution == 25) & (hemisphere == 'n'):
        dims = (448,304)
    elif (proj == 'ps') & (resolution == 25) & (hemisphere == 's'):
        dims = (332,316)
    elif (proj == 'ps') & (resolution == 12.5) & (hemisphere == 'n'):
        dims = (896,608)
    elif (proj == 'ps') & (resolution == 12.5) & (hemisphere == 's'):
        dims = (664,632)
    else:
        print('dims not available')
        raise

    return(dims)

def piomas_grid():

    grids = {}

    for i in ['lon', 'lat']:
        grid = np.array(pd.read_csv(f'read_ice/grid_files/pio_{i}grid.dat', header=None, delim_whitespace=True))

        flat_grid = grid.ravel()

        shaped_grid = flat_grid.reshape(360, 120)

        grids[i] = shaped_grid

    return(grids)


def polar_stereo(resolution, hemisphere):

    """

    Args:
        resolution (int): should be '25' for 25 km
        hemisphere (str): 'n' or 's'

    Returns:
        dictionary of coords, keys: "lon", "lat".
    """

    dims = get_dims(proj='ps', hemisphere=hemisphere, resolution=resolution)

    return_dict = {}

    if resolution == 25: res_code = 25
    elif resolution == 12.5: res_code = 12
    else: raise

    for coord in ['lon', 'lat']:

        grid_dir = f'read_ice/grid_files/ps{hemisphere}{res_code}{coord}s_v3.dat'
        with open(grid_dir, mode='rb') as file:

            # stored as 4-byte integers (little endian) scaled by 100,000

            data = [int.from_bytes(file.read(4), 'little',signed=True)/100_000 for i in range(dims[0]*dims[1])]

            data = np.reshape(data, dims)

        return_dict[coord] = data

    return(return_dict)