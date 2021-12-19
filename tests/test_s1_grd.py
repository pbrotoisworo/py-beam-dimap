import os

import pytest

from PyBeamDimap.reader import BeamDimap

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
    yield BeamDimap(metadata=data3)


def test_data3_important_metadata(dimap):
    """
    Test important metadata parameters
    """
    # Check extracted data is correct
    expected = 'DIMAP'
    assert dimap.metadata_format == expected, assert_error(expected, dimap.metadata_format)

    expected = '2.12.1'
    assert dimap.metadata_version == expected, assert_error(expected, dimap.metadata_version)

    expected = 'Sentinel-1 IW Level-1 GRD Product'
    assert dimap.product_description == expected, assert_error(expected, dimap.product_description)

    expected = 'SENTINEL-1A'
    assert dimap.mission == expected, assert_error(expected, dimap.mission)

    expected = 'S1A_IW_GRDH_1SDV_20211218T204347_20211218T204412_041068_04E104_C5CB_Orb_NR_Cal_TC'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_data3_band_info(dimap):

    actual = dimap.get_band_info(0)['BAND_RASTER_WIDTH']
    expected = '34438'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1)['BAND_RASTER_WIDTH']
    expected = '34438'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['BAND_NAME']
    expected = 'Sigma0_VH'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['BAND_DESCRIPTION']
    expected = None
    assert actual == expected, assert_error(expected, actual)


def test_data3_abstracted_metadata(dimap):

    actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier').text
    expected = 'ESA Sentinel-1 IPF 003.40'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('incidence_near').text
    expected = '30.738478373493205'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PASS').text
    expected = 'DESCENDING'
    assert actual == expected, assert_error(expected, actual)


def test_data3_processing_graph(dimap):

    actual = dimap.get_processing_history(0).operator
    expected = 'Read'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0).parameters['copyMetadata']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(2).parameters['removeThermalNoise']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(3).sources
    expected = 'ThermalNoiseRemoval'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(4).operator
    expected = 'Calibration'
    assert actual == expected, assert_error(expected, actual)



