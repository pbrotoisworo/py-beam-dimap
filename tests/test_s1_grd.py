import os

import pytest

# from PyBeamDimap.reader import BeamDimap
from PyBeamDimap.missions import Sentinel1

TEST_DIR = os.path.abspath('tests')
data3 = os.path.join(TEST_DIR, 'S1_GRDH_Orb_NR_Cal_TC.dim')


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

    expected = 'S1A_IW_GRDH_1SDV_20211218T204347_20211218T204412_041068_04E104_C5CB_Orb_NR_Cal_TC'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_data3_band_info(dimap):

    actual = dimap.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '34438'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1, 'BAND_RASTER_WIDTH')
    expected = '34438'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_NAME')
    expected = 'Sigma0_VH'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_DESCRIPTION')
    expected = None
    assert actual == expected, assert_error(expected, actual)


def test_data3_load_all_band_names(dimap):
    actual = dimap.get_band_info(None, 'BAND_NAME')
    expected = {'0': 'Sigma0_VH', '1': 'Sigma0_VV'}
    assert actual == expected, assert_error(expected, actual)


def test_data3_abstracted_metadata(dimap):

    actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier')['text']
    expected = 'ESA Sentinel-1 IPF 003.40'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier')['desc']
    expected = 'Processing system identifier'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('incidence_near')['text']
    expected = '30.738478373493205'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PASS')['text']
    expected = 'DESCENDING'
    assert actual == expected, assert_error(expected, actual)


def test_data3_processing_graph_with_attributes(dimap):

    actual = dimap.get_processing_history(0, 'operator')
    expected = 'Read'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0, 'parameters')['copyMetadata']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(2, 'parameters')['removeThermalNoise']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(3, 'sources')['sourceProduct']
    expected = 'ThermalNoiseRemoval'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(4, 'operator')
    expected = 'Calibration'
    assert actual == expected, assert_error(expected, actual)


def test_data3_processing_graph_with_nonetypes(dimap):

    # Get list of operators
    actual = dimap.get_processing_history(None, 'operator')
    expected = {
        'node.0': 'Read', 'node.1': 'Apply-Orbit-File', 'node.2': 'ThermalNoiseRemoval',
        'node.3': 'Remove-GRD-Border-Noise', 'node.4': 'Calibration', 'node.5': 'Terrain-Correction',
        'node.6': 'Write'
    }
    assert actual == expected, assert_error(expected, actual)

    # Get all items in second node
    actual = dimap.get_processing_history(1, None)
    expected = {
        'node': 'node.1',
        'id': 'Apply-Orbit-File',
        'operator': 'Apply-Orbit-File',
        'moduleName': 'S1TBX SAR Processing',
        'moduleVersion': '8.0.3',
        'purpose': 'Apply orbit file',
        'authors': 'Jun Lu, Luis Veci',
        'version': '1.0',
        'copyright': 'Copyright (C) 2016 by Array Systems Computing Inc.',
        'processingTime': '2021-12-19T19:26:23.536Z',
        'sources': {'sourceProduct': 'file:/C:/Users/Angelo/Documents/PANJI/Projects/scratch/S1A_IW_GRDH_1SDV_20211218T204347_20211218T204412_041068_04E104_C5CB.zip'},
        'parameters': {'orbitType': 'Sentinel Precise (Auto Download)', 'continueOnFail': 'true', 'polyDegree': '3'}}

    assert actual == expected, assert_error(expected, actual)
