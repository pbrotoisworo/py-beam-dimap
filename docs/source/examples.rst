Usage Examples
==============
Below are some samples of PyBeamDimap usage.

Get file processing history
***************************
Loading processing history of a BEAM-DIMAP file. Processing is logged chronologically and can be accessed by inputting
the index where index 0 is the first operation that was done on the file.

..  code-block:: python
    :caption: Get fifth item in the processing history

        >>> dimap = BeamDimap('S1A.dim')
        >>> history = dimap.get_processing_history(5)
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

..  code-block:: python
    :caption: Get list of operators used

        >>> dimap = BeamDimap('S1A.dim')
        >>> history = dimap.get_processing_history(None, 'operator')
        >>> print(history)
        {'node.0': 'Read',
        'node.1': 'TOPSAR-Split',
        'node.2': 'Apply-Orbit-File',
        'node.3': 'Write',
        'node.4': 'Back-Geocoding',
        'node.5': 'Enhanced-Spectral-Diversity',
        'node.6': 'Write',
        'node.7': 'Read',
        'node.8': 'Interferogram',
        'node.9': 'TOPSAR-Deburst',
        'node.10': 'TopoPhaseRemoval',
        'node.11': 'Multilook',
        'node.12': 'GoldsteinPhaseFiltering',
        'node.13': 'Subset', 'node.14': 'Read',
        'node.15': 'SnaphuImport',
        'node.16': 'Terrain-Correction',
        'node.17': 'BandMaths'
        }

Get band metadata
******************
..  code-block:: python
    :caption: Getting band names for all available bands

        >>> dimap = BeamDimap('S1A.dim')
        >>> band = dimap.get_band_info(None, 'BAND_NAME')
        >>> print(band)
        {'0': 'Sigma0_VH', '1': 'Sigma0_VV'}

..  code-block:: python
    :caption: Getting band metadata

        >>> dimap = BeamDimap('S1A.dim')
        >>> band = dimap.get_band_info(1, 'BAND_RASTER_WIDTH')
        >>> print(band)
        '34438'
