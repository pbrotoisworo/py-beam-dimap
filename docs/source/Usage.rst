Usage
#####
The main entry points for using PyBeamDimap are in ``PyBeamDimap.missions``. Import the relevant Sentinel class for your
particular BEAM-DIMAP (.dim) file.

..  code-block:: python
    :caption: Importing Sentinel-1 class to read Sentinel-1 BEAM-DIMAP files

        >>> from PyBeamDimap.missions import Sentinel1
        >>> dimap = Sentinel1('S1A.dim')

Once you have loaded the BEAM-DIMAP file, access the BEAM-DIMAP sections by accessing the object's properties.
PyBeamDimap is still in development and as of writing the available sections are the following:

* AbstractedMetadata (Sentinel-1 only)
* ProcessingGraph (All missions)
* ImageInterpretation (All missions)


..  code-block:: python
    :caption: Accessing metadata elements in the abstracted metadata section

        >>> mission = dimap.AbstractedMetadata.get_element('MISSION')
        >>> print(mission)
        'SENTINEL-1B'


Usage Examples
==============

Below are some samples of PyBeamDimap usage.

Get file processing history
***************************
Loading processing history of a BEAM-DIMAP file. Processing is logged chronologically and can be accessed by inputting
the index where index 0 is the first operation that was done on the file.

..  code-block:: python
    :caption: Get fifth item in the processing history

        >>> from PyBeamDimap.missions import Sentinel1
        >>> dimap = Sentinel1('S1A.dim', 'SLC')
        >>> history = dimap.ProcessingGraph.get_processing_graph(5)
        >>> print(history)
        {'node': 'node.5',
         'operator': 'Interferogram',
         'moduleName': 'S1TBX InSAR Tools',
         'moduleVersion': '8.0.3',
         'purpose': 'Compute interferograms from stack of coregistered S-1 images',
         'authors': 'Petar Marinkovic, Jun Lu',
         'version': '1.0',
         'copyright': '2021-07-04T15:29:40.799Z',
         'processingTime': None,
         'sources': {'sourceProduct': 'file:/E:/SAR_Iceland/20190809_20190902_Orb_Stack.dim'},
         'parameters':
             {'subtractTopographicPhase': 'false', 'cohWinAz': '2', 'includeCoherence': 'true',
             'srpPolynomialDegree': '5', 'srpNumberPoints': '501', 'cohWinRg': '10',
             'outputElevation': 'false', 'outputLatLon': 'false', 'orbitDegree': '3',
             'squarePixel': 'true', 'subtractFlatEarthPhase': 'true',
             'tileExtensionPercent': '100', 'externalDEMApplyEGM': 'false',
             'demName': 'SRTM 1Sec HGT', 'externalDEMNoDataValue': '0.0'}
        }

Get list of bands
*****************
..  code-block:: python
    :caption: Get list of operators used

        >>> from PyBeamDimap.missions import Sentinel2
        >>> dimap = Sentinel2('S2A.dim', '2A')
        >>> bands = dimap.ImageInterpretation.get_band_info(None, 'BAND_NAME')
        >>> print(bands)
        {
        '0': 'B1', '1': 'B2', '2': 'B3', '3': 'B4', '4': 'B5', '5': 'B6', '6': 'B7', '7': 'B8', '8': 'B8A', '9': 'B9',
        '10': 'B11', '11': 'B12', '12': 'quality_aot', '13': 'quality_wvp', '14': 'quality_cloud_confidence',
        '15': 'quality_snow_confidence', '16': 'quality_scene_classification', '17': 'view_zenith_mean',
        '18': 'view_azimuth_mean', '19': 'sun_zenith', '20': 'sun_azimuth', '21': 'view_zenith_B1',
        '22': 'view_azimuth_B1', '23': 'view_zenith_B2', '24': 'view_azimuth_B2', '25': 'view_zenith_B3',
        '26': 'view_azimuth_B3', '27': 'view_zenith_B4', '28': 'view_azimuth_B4', '29': 'view_zenith_B5',
        '30': 'view_azimuth_B5', '31': 'view_zenith_B6', '32': 'view_azimuth_B6', '33': 'view_zenith_B7',
        '34': 'view_azimuth_B7', '35': 'view_zenith_B8', '36': 'view_azimuth_B8', '37': 'view_zenith_B8A',
        '38': 'view_azimuth_B8A', '39': 'view_zenith_B9', '40': 'view_azimuth_B9', '41': 'view_zenith_B10',
        '42': 'view_azimuth_B10', '43': 'view_zenith_B11', '44': 'view_azimuth_B11', '45': 'view_zenith_B12',
        '46': 'view_azimuth_B12'
        }

Get band metadata
******************
..  code-block:: python
    :caption: Getting band metadata

        >>> from PyBeamDimap.missions import Sentinel1
        >>> dimap = Sentinel1('S1A.dim')
        >>> band = dimap.ImageInterpretation.get_band_info(1, 'BAND_RASTER_WIDTH')
        >>> print(band)
        '34438'

Load Sentinel-1 orbit state vectors
***********************************
..  code-block:: python
    :caption: Getting band metadata

        >>> from PyBeamDimap.missions import Sentinel1

        >>> dimap = Sentinel1('S1A.dim')
        >>> df = dimap.AbstractedMetadata.orbit_state_vectors
        >>> print(df)

The print results are seen below. The dataframe shown is a truncated version for documentation preview purposes only.

+-------+---------------------------+---------------------------+---------------------------+
|       | orbit_vector1             | orbit_vector2             | orbit_vector3             |
+=======+===========================+===========================+===========================+
| time  | 02-SEP-2019 07:57:47.909  | 02-SEP-2019 07:57:48.909  | 02-SEP-2019 07:57:49.909  |
+-------+---------------------------+---------------------------+---------------------------+
| x_pos | 3085342.724               | 3090982.677               | 3096618.594               |
+-------+---------------------------+---------------------------+---------------------------+
| y_pos | -691610.5336              | -695560.998               | -699511.5057              |
+-------+---------------------------+---------------------------+---------------------------+
| z_pos | 6320008.356               | 6316825.3                 | 6313635.119               |
+-------+---------------------------+---------------------------+---------------------------+
| x_vel | 5641.969699               | 5637.9358                 | 5633.895573               |
+-------+---------------------------+---------------------------+---------------------------+
| y_vel | -3950.440933              | -3950.486919              | -3950.527891              |
+-------+---------------------------+---------------------------+---------------------------+
| z_vel | -3179.492029              | -3186.619094              | -3193.742584              |
+-------+---------------------------+---------------------------+---------------------------+
