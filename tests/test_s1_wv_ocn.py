import os

import pytest

# from PyBeamDimap.reader import BeamDimap
from PyBeamDimap.missions import Sentinel1

TEST_DIR = os.path.abspath('tests')
data3 = os.path.join(TEST_DIR, 'S1_WV_OCN_extractor.dim')


def assert_error(expected, actual):
    return f'Error with extracted XML value. Expecting {expected}. Got {actual}.'


@pytest.fixture
def dimap():
    """
    Load an instance of BEAM-DIMAP reader with single band SLC data
    """
    # Setup testing environment
    yield Sentinel1(metadata=data3, product='GRD')


def test_data3_important_metadata(dimap):
    """
    Test important metadata parameters
    """
    # Check extracted data is correct
    expected = 'DIMAP'
    assert dimap.metadata_format == expected, assert_error(expected, dimap.metadata_format)

    expected = '2.12.1'
    assert dimap.metadata_version == expected, assert_error(expected, dimap.metadata_version)

    expected = 'SENTINEL-1A'
    assert dimap.mission == expected, assert_error(expected, dimap.mission)

    expected = 'S1A_WV_OCN__2SSV_20211224T163127_20211224T170555_041153_04E3D3_7BE5_extractor'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_data3_band_info(dimap):

    actual = dimap.ImageInterpretation.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '20'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(0, 'BAND_NAME')
    expected = 'vv_001_owiWindSpeed'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(0, 'BAND_DESCRIPTION')
    expected = 'SAR Wind speed'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(1, 'BAND_DESCRIPTION')
    expected = 'SAR Wind direction (meteorological convention= clockwise direction from where the wind comes respect to North)'
    assert actual == expected, assert_error(expected, actual)


def test_nested_abstracted_metadata_sections(dimap):

    # Orbit state vectors
    actual = dimap.AbstractedMetadata.orbit_state_vectors
    expected = None
    assert actual == expected, assert_error(expected, actual)

    # Doppler centroid coeffs
    actual = dimap.AbstractedMetadata.doppler_centroid_coeffs
    expected = None
    assert actual == expected, assert_error(expected, actual)

    # Baselines
    actual = dimap.AbstractedMetadata.baselines
    expected = None
    assert actual == expected, assert_error(expected, actual)

    # Orbit offsets
    actual = dimap.AbstractedMetadata.orbit_offsets
    expected = None
    assert actual == expected, assert_error(expected, actual)

    # Look direction
    actual = dimap.AbstractedMetadata.look_directions
    expected = None
    assert actual == expected, assert_error(expected, actual)

    # ESD measurement
    actual = dimap.AbstractedMetadata.EsdMeasurement.dataframe(verbose=False)
    expected = None
    assert actual == expected, assert_error(expected, actual)


def test_data3_load_all_band_names(dimap):
    actual = dimap.ImageInterpretation.get_band_info(None, 'BAND_NAME')
    expected = {'0': 'vv_001_owiWindSpeed',
                '1': 'vv_001_owiWindDirection',
                '2': 'vv_001_owiEcmwfWindSpeed',
                '3': 'vv_001_owiEcmwfWindDirection'
                }
    assert actual == expected, assert_error(expected, actual)


def test_data3_abstracted_metadata(dimap):

    actual = dimap.AbstractedMetadata.get_attribute('Processing_system_identifier')
    expected = 'ESA Sentinel-1 IPF 003.40'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.get_attribute('Processing_system_identifier', 'Description')
    expected = 'Processing system identifier'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.get_attribute('incidence_near')
    expected = '99999.0'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.get_attribute('PASS')
    expected = 'DESCENDING'
    assert actual == expected, assert_error(expected, actual)


def test_data3_processing_graph_with_attributes(dimap):

    actual = dimap.ProcessingGraph.get_processing_graph(0, 'operator')
    expected = 'BandsExtractorOp'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(0, 'parameters')['sourceBandNames']
    expected = 'vv_001_owiWindSpeed,vv_001_owiWindDirection,vv_001_owiEcmwfWindSpeed,vv_001_owiEcmwfWindDirection'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(1, 'operator')
    expected = 'Write'
    assert actual == expected, assert_error(expected, actual)


def test_data3_processing_graph_with_nonetypes(dimap):

    # Get list of operators
    actual = dimap.ProcessingGraph.get_processing_graph(None, 'operator')
    expected = {
        'node.0': 'BandsExtractorOp',
        'node.1': 'Write'
    }
    assert actual == expected, assert_error(expected, actual)

    # Get all items in second node
    actual = dimap.ProcessingGraph.get_processing_graph(1, None)
    expected = {
        'node': 'node.1',
        'id': 'Write$17DF0563EEC',
        'operator': 'Write',
        'moduleName': 'SNAP Graph Processing Framework (GPF)',
        'moduleVersion': '8.0.3',
        'purpose': 'Writes a data product to a file.',
        'authors': 'Marco Zuehlke, Norman Fomferra',
        'version': '1.3',
        'copyright': '(c) 2010 by Brockmann Consult',
        'processingTime': '2021-12-25T06:45:23.821Z',
        'sources': {'sourceProduct': r'file:/C:/Users/Angelo/Documents/PANJI/Projects/beam-dimap-reader/S1A_WV_OCN__2SSV_20211224T163127_20211224T170555_041153_04E3D3_7BE5_extractor.dim'},
        'parameters': {'writeEntireTileRows': 'true',
                       'file': r'C:\Users\Angelo\Documents\PANJI\Projects\beam-dimap-reader\S1A_WV_OCN__2SSV_20211224T163127_20211224T170555_041153_04E3D3_7BE5_extractor.dim',
                       'deleteOutputOnFailure': 'true',
                       'formatName': 'BEAM-DIMAP',
                       'clearCacheAfterRowWrite': 'false'}
    }

    assert actual == expected, assert_error(expected, actual)
