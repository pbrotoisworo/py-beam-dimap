# py-beam-dimap-reader
[![Build Status](https://app.travis-ci.com/pbrotoisworo/py-beam-dimap.svg?branch=main)](https://app.travis-ci.com/pbrotoisworo/py-beam-dimap)


A Python interface to easily parse and interact with the BEAM-DIMAP XML file which is used as part of SNAP software for Sentinel satellites.

The metadata parameters are parsed and structured as a Python dictionary for easier navigation. 
# Features
* Extract processing history including operator used and the parameters used
* Extract metadata attributes

# Usage
Below is sample usage with Sentinel-1 metadata.
```py
from pybeamdimap import BeamDimap

dim_file = 'Sentinel1_SLC.dim'
dimap = BeamDimap(dim_file)

# Look at 11th item in the processing history
dimap.get_processing_history(11).operator  # Multilook
dimap.get_processing_history(11).parameters['nAzLooks']  # 2

# Get mission
dimap.get_abstracted_metadata('MISSION')
# {'@name': 'MISSION', '@desc': 'Satellite mission', '@unit': '', '@type': 'ascii', '@mode': 'rw', '#text': 'SENTINEL-1B'}
dimap.get_abstracted_metadata('MISSION').text
# 'SENTINEL-1B
```