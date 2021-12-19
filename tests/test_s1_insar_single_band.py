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


    actual = dimap.get_band_info(0)['BAND_RASTER_WIDTH']
    expected = '2522'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['BAND_RASTER_WIDTH']
    expected = '2522'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['BAND_RASTER_HEIGHT']
    expected = '1125'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['DATA_TYPE']
    expected = 'float32'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['NO_DATA_VALUE_USED']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)


def test_data1_abstracted_metadata(dimap):

    actual = dimap.get_abstracted_metadata_attribute('SWATH').text
    expected = 'IW2'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PRODUCT').text
    expected = 'S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('incidence_near').text
    expected = '35.995479583740234'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('centre_lat').text
    expected = '64.27266071634527'
    assert actual == expected, assert_error(expected, actual)


@pytest.mark.xfail
def test_data1_get_invalid_band(dimap):
    """
    This should fail because this is testing a single band image
    """
    dimap.get_band_info(1)


def test_data1_processing_graph(dimap):

    actual = dimap.get_processing_history(0).operator
    expected = 'Read'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0).parameters['copyMetadata']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(11).parameters['nAzLooks']
    expected = '2'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1).operator
    expected = 'TOPSAR-Split'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(2).sources
    expected = 'product:S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1).sources
    expected = 'file:/E:/SAR_Iceland/images/S1B_IW_SLC__1SDV_20190809T075740_20190809T075807_017506_020EC0_4DA0.zip'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)
