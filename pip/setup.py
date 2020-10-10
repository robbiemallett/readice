import setuptools

setuptools.setup(
    name="read_ice",
    version="0.0.4",
    description='Tool for extracting polar data from tricky files',
    author="Robbie Mallett",
    author_email="robbie.mallett.17@ucl.co.uk",
    url="https://github.com/robbiemallett/read_ice",
    install_requires=['pandas',
                      'numpy',
                      'scipy',
                      'matplotlib',
                      'docutils',
                      'pyproj',
                      'xarray'
                      'Pygments',
                      'netCDF4',
                      'cartopy'],
    python_requires='>=3.6',
)