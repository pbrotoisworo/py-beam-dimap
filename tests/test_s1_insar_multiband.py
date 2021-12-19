import os

import pytest

from PyBeamDimap.reader import BeamDimap

TEST_DIR = os.path.abspath('tests')
data2 = os.path.join(TEST_DIR, 'S1_DInSARStack_20190902_20190914.dim')


def assert_error(expected, actual):
    return f'Error with extracted XML value. Expecting {expected}. Got {actual}.'


#######################################
# Test multiband Sentinel-1 SLC data
#######################################

@pytest.fixture
def dimap():
    """
    Load an instance of BEAM-DIMAP reader with single band SLC data
    """
    # Setup testing environment
    yield BeamDimap(metadata=data2)


def test_data2_important_metadata(dimap):
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

    expected = '20190902_20190914_DInSARStack'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_data2_band_info(dimap):

    actual = dimap.get_band_info(0)['BAND_RASTER_WIDTH']
    expected = '5282'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1)['BAND_RASTER_WIDTH']
    expected = '5282'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(5)['BAND_DESCRIPTION']
    expected = None
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0)['BAND_NAME']
    expected = 'Intensity_ifg_VV_02Sep2019_14Sep2019'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1)['BAND_NAME']
    expected = 'Intensity_ifg_VV_02Sep2019_14Sep2019_db'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(2)['BAND_NAME']
    expected = 'Phase_ifg_VV_02Sep2019_14Sep2019'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(3)['BAND_NAME']
    expected = 'coh_IW2_VV_02Sep2019_14Sep2019'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(4)['BAND_NAME']
    expected = 'Unw_Phase_ifg_02Sep2019_14Sep2019_VV'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(5)['BAND_NAME']
    expected = 'displacement_VV_slv1_02Sep2019'
    assert actual == expected, assert_error(expected, actual)


def test_data2_abstracted_metadata(dimap):

    actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier').text
    expected = 'ESA Sentinel-1 IPF 003.10'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PRODUCT').text
    expected = 'S1B_IW_SLC__1SDV_20190902T075741_20190902T075808_017856_0219A5_70FA'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PASS').text
    expected = 'DESCENDING'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('centre_lat').text
    expected = '64.27210588794522'
    assert actual == expected, assert_error(expected, actual)


def test_data1_processing_graph(dimap):

    actual = dimap.get_processing_history(0).operator
    expected = 'Read'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0).parameters['copyMetadata']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(4).parameters['resamplingType']
    expected = 'BILINEAR_INTERPOLATION'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(5).operator
    expected = 'Enhanced-Spectral-Diversity'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(4).sources
    expected = 'file:/E:/SAR_Iceland/sample/20190902_Orb.dim'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)
    expected = 'file:/E:/SAR_Iceland/sample/20190914_Orb.dim'
    assert actual['sourceProduct.1'] == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(1).sources
    expected = 'file:/E:/SAR_Iceland/images/S1B_IW_SLC__1SDV_20190902T075741_20190902T075808_017856_0219A5_70FA.zip'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(17).sources
    expected = 'file:/E:/SAR_Iceland/sample/20190902_20190914_Orb_Stack_Ifg_Deb_TopoPhase_ML_Flt_Unw_TC.dim'
    assert actual['sourceProduct.0'] == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(17).sources
    expected = 'file:/E:/SAR_Iceland/sample/20190902_20190914_disp_TC.dim'
    assert actual['sourceProduct.1'] == expected, assert_error(expected, actual)