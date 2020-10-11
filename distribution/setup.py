import setuptools

setuptools.setup(
    name="readice",
    version="0.0.6",
    description='Tool for extracting polar data from tricky files',
    author="Robbie Mallett",
    author_email="robbie.mallett.17@ucl.co.uk",
    url="https://github.com/robbiemallett/read_ice",
    install_requires=['pandas',
                      'numpy',
                      'matplotlib',
                      'pyproj',
                      'xarray',
                      'Pygments',
                      'netCDF4',
                      'cartopy'],
    python_requires='>=3.6',
)