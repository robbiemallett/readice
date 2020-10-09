import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="read_ice",
    version="0.0.1",
    author="Robbie Mallett",
    author_email="robbie.mallett.17@ucl.co.uk",
    description="A package for reading tricky polar data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robbiemallett/read_ice",
    install_requires=['pandas',
                      'numpy',
                      'scipy',
                      'matplotlib',
                      'docutils',
                      'Pygments',
                      'netCDF4',
                      'cartopy'],
    python_requires='>=3.6',
)