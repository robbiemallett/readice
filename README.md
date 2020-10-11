
# read_ice
A package to read and plot polar data from binary (and other) formats.

[![Documentation Status](https://readthedocs.org/projects/read-ice/badge/?version=latest)](https://read-ice.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/robbiemallett/read_ice.svg?branch=main)](https://travis-ci.org/robbiemallett/read_ice) [![PyPI version](https://badge.fury.io/py/read-ice.svg)](https://badge.fury.io/py/read-ice)

## Installation

Currently the best way to install read_ice is to use the package manager [pip](https://pip.pypa.io/en/stable/). Note that the pip distribution has a hyphen (-) instead of an underscore (_). A conda distribution is imminent!

```bash
pip install read-ice
```
## Documentation & Walkthrough

You can find the documentation for read_ice [here](https://read-ice.readthedocs.io/en/latest/) and a walkthrough video [here](https://www.youtube.com/watch?v=WXEUVK0xgfY).

## Contributing Your Code
If you have written code to read sea ice files then **please** open a pull request and add it to the package! If you've never done this before, it's easy: [here's a walkthrough for beginners](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3/).

To make your code a full part of the package you'll need to include an example file that your code can read (which lives in `read_ice/tests/test_files`), and if it uses a new grid that read_ice didn't previously support, you should include this in `read_ice/grid_files`. The code to read your example file should be a function inside `read_ice/read_file.py` and code that returns the coordinates (if the coordinates are new to read_ice) should be contained within `get_geo_coords.py`. Your function that gets the data must do two things: return the data as a numpy array (2D or 3D if there's a time axis), and in the case `with_coords = True` it must return a dictionary with the data array, and the lon/lat coordinates for the data (a 2D array for each `lon` and `lat` dict key.

If you contribute code it would be great if you could also write *tests* for that code, but this is not compulsory for a PR. read_ice already has several tests built in, so you just need to follow the template. You'll probably just be adding code to the read_file and read_geo_coords modules, so just build on those. Here's [a great guide](https://www.youtube.com/watch?v=6tNS--WetLI) to how Python's *unittest* module works and how to make your own.

## License
This project has a highly permissive [MIT licence](https://github.com/robbiemallett/read_ice/blob/master/LICENCE.txt). If you'd like to incorporate read_ice into your package, that's great - just do it! If you want to chat about this first then I'm happy to, particularly as read_ice hasn't hit v1.0.0 yet, so function names etc. still might change. 
