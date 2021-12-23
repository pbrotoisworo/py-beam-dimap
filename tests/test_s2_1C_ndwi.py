# Test Sentinel-2 Level 1C data

import os

import pytest

from PyBeamDimap.missions import Sentinel2

TEST_DIR = os.path.abspath('tests')
data = os.path.join(TEST_DIR, 'S2_1C_ndwi.dim')


def assert_error(expected, actual):
    return f'Error with extracted XML value. Expecting {expected}. Got {actual}.'


@pytest.fixture
def dimap():
    """
    Load an instance of BEAM-DIMAP reader with single band SLC data
    """
    # Setup testing environment
    yield Sentinel2(metadata=data, product_type='1C')


def test_important_metadata(dimap):
    """
    Test important metadata parameters
    """
    # Check extracted data is correct
    expected = 'DIMAP'
    assert dimap.metadata_format == expected, assert_error(expected, dimap.metadata_format)

    expected = '2.12.1'
    assert dimap.metadata_version == expected, assert_error(expected, dimap.metadata_version)

    expected = None  # None because there is no explicit mention of the mission in 1C data
    assert dimap.mission == expected, assert_error(expected, dimap.mission)

    expected = 'S2B_MSIL1C_20211203T022049_N0301_R003_T51PTS_20211203T042026_ndwi'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_band_info(dimap):

    actual = dimap.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '5490'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_NAME')
    expected = 'ndwi'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_DESCRIPTION')
    expected = None
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1, 'BAND_DESCRIPTION')
    expected = 'ndwi specific flags'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1, 'IMAGE_TO_MODEL_TRANSFORM')
    expected = '20.0,0.0,0.0,-20.0,199980.0,1700040.0'
    assert actual == expected, assert_error(expected, actual)


def test_load_all_band_names(dimap):
    actual = dimap.get_band_info(None, 'BAND_NAME')
    expected = {'0': 'ndwi', '1': 'flags'}
    assert actual == expected, assert_error(expected, actual)


def test_processing_graph_with_attributes(dimap):

    actual = dimap.get_processing_history(0, 'operator')
    expected = 'NdwiOp'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1, 'operator')
    expected = 'Write'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0, 'parameters')['upsampling']
    expected = 'Nearest'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1, 'sources')['sourceProduct']
    expected = 'file:/C:/Users/Angelo/Documents/PANJI/Projects/beam-dimap-reader/S2B_MSIL1C_20211203T022049_N0301_R003_T51PTS_20211203T042026_ndwi.dim'
    assert actual == expected, assert_error(expected, actual)

