# PyBeamDimap
[![Build Status](https://app.travis-ci.com/pbrotoisworo/py-beam-dimap.svg?branch=main)](https://app.travis-ci.com/pbrotoisworo/py-beam-dimap)
[![codecov](https://codecov.io/gh/pbrotoisworo/py-beam-dimap/branch/main/graph/badge.svg?token=3FB366IFP7)](https://codecov.io/gh/pbrotoisworo/py-beam-dimap)
[![Documentation Status](https://readthedocs.org/projects/py-beam-dimap/badge/?version=latest)](https://py-beam-dimap.readthedocs.io/en/latest/?badge=latest)

A Python interface to easily parse and interact with the BEAM-DIMAP XML file which is used as part of SNAP software for
Sentinel satellites. The metadata parameters are parsed and structured as a Python dictionary for easier navigation.

Visit the [ReadTheDocs page](https://py-beam-dimap.readthedocs.io/en/latest/index.html) for more information on how to 
use this software. 

# Features
* Extract processing history including operator used and the parameters used
* Extract metadata attributes

# Installation
In the project root type `pip install .` to run the `setup.py` file.

# Usage
Below is sample usage with Sentinel-1 metadata.
```py
from PyBeamDimap.missions import Sentinel1

dim_file = 'Sentinel1_SLC.dim'
dimap = Sentinel1(dim_file, 'SLC')

# Look at 11th item in the processing history
dimap.get_processing_history(11, 'operator')  # Multilook
dimap.get_processing_history(11, 'parameters')['nAzLooks']  # 2

# Get mission
dimap.get_abstracted_metadata('MISSION')['text']
# 'SENTINEL-1B
```