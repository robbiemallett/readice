
# readice
A package to read and plot polar data from binary (and other) formats.

[![Documentation Status](https://readthedocs.org/projects/readice/badge/?version=latest)](https://read-ice.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/robbiemallett/readice.svg?branch=main)](https://travis-ci.org/robbiemallett/readice) [![PyPI version](https://badge.fury.io/py/read-ice.svg)](https://badge.fury.io/py/read-ice)

## Installation

Currently the best way to install readice is to use the package manager [pip](https://pip.pypa.io/en/stable/). A conda distribution is imminent!

```bash
pip install read-ice
```
## Documentation & Walkthrough

You can find the documentation for readice [here](https://read-ice.readthedocs.io/en/latest/) and a walkthrough video [here](https://www.youtube.com/watch?v=WXEUVK0xgfY).

There are currently three parts of readice: `read_file.py` which serves up data from files `get_geo_coords.py`, which gets the relevant longitude/latitude arrays for the data, and `tools.py` code. `tools` includes code to output netcdf4 files and plotting data with Cartopy. 

### Example code to extract SSMI brightness temperature data from an NSIDC binary file, plot it and save it as a netcdf

```python

from readice.read_file import SSMI_Tb
from readice.tools import plot, dict_to_nc

# First get the data out of the file. We must specify the location of the file to do this.

# We also want to get the geocoordinates for plotting etc., and those depend on the frequency and the hemisphere.
# So we supply those to SSMI_Tb too.
# In order to tell the function to give us the geocoordinates as well as the data itself, we set with_coords=True.

information = SSMI_Tb(file_location='tests/test_files/tb_f17_20190711_v5_n37h.bin',
                hemisphere='n',
                frequency=37,
                with_coords=True)

# Because with_coords=True, information is a dictionary with keys 'data', 'lon', 'lat'. All 2D numpy arrays in this case.
# If with_coords=False, information would just be a 2D numpy array of the data in the binary file, with no grid.

# the plot function uses cartopy and the matplotlib pcolormesh method. 
# All three arguments to the function must be 2D arrays. These should be arrays of the same shape.
# Check out the documentation for how to specify the colormap, scale min and max, bounding latitude and more.

plot(information['lon'], information['lat'], information['data'])

# the dict_to_nc function creates a simple netcdf file with xarray. The function *must take* data in the dictionary format output by the read_file.py script.
# If you want to specify the contents of this (say, a 365 day long data array for daily data in a year), that's fine. Just keep it in the dict format.
# You must specify the name of the variable with the variable_name argument. 
# Other attributes (e.g. year, author) can be supplied in a separate dictionary with the attributes argument (see docs).

dict_to_nc(input_dict=information, 
           output_file_destination='../test.nc',
           variable_name='Brightness Temperature')

```

## Contributing Your Code
If you have written code to read sea ice files then **please** open a pull request and add it to the package! If you've never done this before, it's easy: [here's a walkthrough for beginners](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3/).

To make your code a full part of the package you'll need to include an example file that your code can read (which lives in `readice/tests/test_files`), and if it uses a new grid that readice didn't previously support, you should include this in `readice/grid_files`. The code to read your example file should be a function inside `readice/read_file.py` and code that returns the coordinates (if the coordinates are new to readice) should be contained within `get_geo_coords.py`. Your function that gets the data must do two things: return the data as a numpy array (2D or 3D if there's a time axis), and in the case `with_coords = True` it must return a dictionary with the data array, and the lon/lat coordinates for the data (a 2D array for each `lon` and `lat` dict key.

If you contribute code it would be great if you could also write *tests* for that code, but this is not compulsory for a PR. readice already has several tests built in, so you just need to follow the template. You'll probably just be adding code to the read_file and read_geo_coords modules, so just build on those. Here's [a great guide](https://www.youtube.com/watch?v=6tNS--WetLI) to how Python's *unittest* module works and how to make your own.

## License
This project has a highly permissive [MIT licence](https://github.com/robbiemallett/readice/blob/master/LICENCE.txt). If you'd like to incorporate readice into your package, that's great - just do it! If you want to chat about this first then I'm happy to, particularly as readice hasn't hit v1.0.0 yet, so function names etc. still might change. 
