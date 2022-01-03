# Test Sentinel-2 Level 1C data

import os

import pytest

from PyBeamDimap.missions import Sentinel2

TEST_DIR = os.path.abspath('tests')
data = os.path.join(TEST_DIR, 'S2_2A_msk.dim')


def assert_error(expected, actual):
    return f'Error with extracted XML value. Expecting {expected}. Got {actual}.'


@pytest.fixture
def dimap():
    """
    Load an instance of BEAM-DIMAP reader with single band SLC data
    """
    # Setup testing environment
    yield Sentinel2(metadata=data, product_type='2A')


def test_important_metadata(dimap):
    """
    Test important metadata parameters
    """
    # Check extracted data is correct
    expected = 'DIMAP'
    assert dimap.metadata_format == expected, assert_error(expected, dimap.metadata_format)

    expected = '2.12.1'
    assert dimap.metadata_version == expected, assert_error(expected, dimap.metadata_version)

    expected = 'Sentinel-2A'
    assert dimap.mission == expected, assert_error(expected, dimap.mission)

    expected = 'S2A_MSIL2A_20211219T033141_N0301_R018_T48PUT_20211219T055114_msk'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_band_info(dimap):

    actual = dimap.ImageInterpretation.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '1830'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(1, 'BAND_RASTER_WIDTH')
    expected = '10980'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(5, 'BAND_DESCRIPTION')
    expected = 'Reflectance in band B6'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(4, 'SCALING_FACTOR')
    expected = '1.0E-4'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(6, 'BAND_NAME')
    expected = 'B7'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(6, 'DATA_TYPE')
    expected = 'uint16'
    assert actual == expected, assert_error(expected, actual)


def test_load_all_band_names(dimap):
    actual = dimap.ImageInterpretation.get_band_info(None, 'BAND_NAME')
    expected = {
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
        '46': 'view_azimuth_B12'}
    assert actual == expected, assert_error(expected, actual)


def test_processing_graph_with_attributes(dimap):

    actual = dimap.ProcessingGraph.get_processing_graph(0, 'operator')
    expected = 'Land-Sea-Mask'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(0, 'parameters')['landMask']
    expected = 'false'
    assert actual == expected, assert_error(expected, actual)
