import os

import pytest

from PyBeamDimap.reader import BeamDimap

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STSA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'py-beam-dimap')
TESTS_DIR = os.path.abspath('tests')

TEST_DIR = os.path.abspath('tests')
data1 = os.path.join(TEST_DIR, 'S1_coherance.dim')


def assert_error(expected, actual):
    return f'Error with extracted XML value. Expecting {expected}. Got {actual}.'


#######################################
# Test single band Sentinel-1 SLC data
#######################################

@pytest.fixture
def dimap():
    """
    Load an instance of BEAM-DIMAP reader with single band SLC data
    """
    # Setup testing environment
    yield BeamDimap(metadata=data1)


def test_data1_important_metadata(dimap):
    """
    Test important metadata parameters
    """
    # Check extracted data is correct
    expected = 'DIMAP'
    assert dimap.metadata_format == expected, assert_error(expected, dimap.metadata_format)

    expected = '2.12.1'
    assert dimap.metadata_version == expected, assert_error(expected, dimap.metadata_version)

    expected = 'Sentinel-1 IW Level-1 SLC Product'
    assert dimap.product_description == expected, assert_error(expected, dimap.product_description)

    expected = 'SENTINEL-1B'
    assert dimap.mission == expected, assert_error(expected, dimap.mission)

    expected = '20190809_20190902_coh_tc'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_data1_band_info(dimap):

    actual = dimap.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '2522'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '2522'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_RASTER_HEIGHT')
    expected = '1125'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'DATA_TYPE')
    expected = 'float32'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'NO_DATA_VALUE_USED')
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)


def test_data1_load_all_band_names(dimap):
    actual = dimap.get_band_info(None, 'BAND_NAME')
    expected = {'0': 'coh_IW2_VV_09Aug2019_02Sep2019'}
    assert actual == expected, assert_error(expected, actual)


def test_data1_abstracted_metadata(dimap):

    actual = dimap.get_abstracted_metadata_attribute('SWATH')
    expected = 'IW2'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PRODUCT')
    expected = 'S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('incidence_near')
    expected = '35.995479583740234'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('centre_lat')
    expected = '64.27266071634527'
    assert actual == expected, assert_error(expected, actual)


@pytest.mark.xfail
def test_data1_get_invalid_band(dimap):
    """
    This should fail because this is testing a single band image
    """
    dimap.get_band_info(1)


def test_data1_processing_graph_with_attributes(dimap):

    actual = dimap.get_processing_history(0, 'operator')
    expected = 'Read'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0, 'parameters')['copyMetadata']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(11, 'parameters')['nAzLooks']
    expected = '2'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1, 'operator')
    expected = 'TOPSAR-Split'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(2, 'sources')
    expected = 'product:S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1, 'sources')
    expected = 'file:/E:/SAR_Iceland/images/S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0.zip'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)


def test_data1_processing_graph_with_nonetypes(dimap):

    # Get list of operators
    actual = dimap.get_processing_history(None, 'operator')
    expected = {'node.0': 'Read', 'node.1': 'TOPSAR-Split', 'node.2': 'Apply-Orbit-File', 'node.3': 'Write',
                'node.4': 'Back-Geocoding', 'node.5': 'Enhanced-Spectral-Diversity', 'node.6': 'Write',
                'node.7': 'Read', 'node.8': 'Interferogram', 'node.9': 'TOPSAR-Deburst', 'node.10': 'TopoPhaseRemoval',
                'node.11': 'Multilook', 'node.12': 'GoldsteinPhaseFiltering', 'node.13': 'Subset', 'node.14': 'Read',
                'node.15': 'SnaphuImport', 'node.16': 'Terrain-Correction', 'node.17': 'BandMaths'}
    assert actual == expected, assert_error(expected, actual)

    # Get all items in third node
    actual = dimap.get_processing_history(2, None)
    expected = {'node': 'node.2', 'operator': 'Apply-Orbit-File', 'moduleName': 'S1TBX SAR Processing',
                'moduleVersion': '8.0.3', 'purpose': 'Apply orbit file', 'authors': 'Jun Lu, Luis Veci',
                'version': '1.0', 'copyright': 'Copyright (C) 2016 by Array Systems Computing Inc.',
                'processingTime': '2021-07-04T15:27:51.595Z',
                'sources': {'sourceProduct': 'product:S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0'},
                'parameters': {'orbitType': 'Sentinel Precise (Auto Download)', 'continueOnFail': 'true', 'polyDegree': '3'}}
    assert actual == expected, assert_error(expected, actual)

