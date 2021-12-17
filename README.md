# py-beam-dimap-reader
A Python interface to easily parse and interact with the BEAM-DIMAP XML file which is used as part of SNAP software for Sentinel satellites.

The metadata parameters are parsed and structured as a Python dictionary for easier navigation. 
# Features
* Extract processing history including operator used and the parameters used
* Extract metadata text

# Usage

```py
dim_file = 'Sentinel1_SLC.dim'
dimap = BeamDimap(dim_file)

# Get 11th item in the processing history
dimap.get_processing_history(11)
# {'node': 'node.11', 'operator': 'Multilook', 'parameters': {'nAzLooks': '2', 'nRgLooks': '6', 'outputIntensity': 'false', 'grSquarePixel': 'true'}}

# Get mission
dimap.get_abstracted_metadata('MISSION')
# {'@name': 'MISSION', '@desc': 'Satellite mission', '@unit': '', '@type': 'ascii', '@mode': 'rw', '#text': 'SENTINEL-1B'}

```