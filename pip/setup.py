import setuptools

setuptools.setup(
    name="read_ice",
    version="0.0.1",
    author="Robbie Mallett",
    packages=['read_ice'],
    author_email="robbie.mallett.17@ucl.co.uk",
    url="https://github.com/robbiemallett/read_ice",
    install_requires=['pandas',
                      'numpy',
                      'scipy',
                      'matplotlib',
                      'docutils',
                      'pyproj',
                      'Pygments',
                      'netCDF4',
                      'cartopy'],
    python_requires='>=3.6',
)