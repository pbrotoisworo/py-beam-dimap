# PyBeamDimap
[![Build Status](https://app.travis-ci.com/pbrotoisworo/py-beam-dimap.svg?branch=main)](https://app.travis-ci.com/pbrotoisworo/py-beam-dimap)
[![codecov](https://codecov.io/gh/pbrotoisworo/py-beam-dimap/branch/main/graph/badge.svg?token=3FB366IFP7)](https://codecov.io/gh/pbrotoisworo/py-beam-dimap)
[![Documentation Status](https://readthedocs.org/projects/py-beam-dimap/badge/?version=latest)](https://py-beam-dimap.readthedocs.io/en/latest/?badge=latest)

A Python interface to easily parse and interact with the BEAM-DIMAP XML file which is used as part of SNAP software for
Sentinel satellites. The metadata parameters are parsed and structured as a Python dictionary for easier navigation.

Visit the [ReadTheDocs page](https://py-beam-dimap.readthedocs.io/en/latest/index.html) for more information on how to 
use this software. 

# Features
* Quickly and easily navigate the BEAM-DIMAP metadata for Sentinel satellites
* Metadata sections are available in preprocessed dataframes or dictionary objects
* Tested against many workflows. If it raises an issue with your particular workflow please raise an issue. 

# Installation
Open the terminal and type:
```
pip install git+https://github.com/pbrotoisworo/py-beam-dimap
```

# Contributing
Contributing can be done by submitting a pull request or even just raising an issue. If you encounter an error
please let me know.

If you are submitting a pull request, ensure that it passes the tests by installing `pytest` and typing the
following command from the project root:
```
pytest tests
``` 