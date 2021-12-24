import os

import pytest

from PyBeamDimap.missions import Sentinel1

TEST_DIR = os.path.abspath('tests')
data = os.path.join(TEST_DIR, 'S1_EW_GRD_Orb_Cal_Spk.dim')


def assert_error(expected, actual):
    return f'Error with extracted XML value. Expecting {expected}. Got {actual}.'


@pytest.fixture
def dimap():
    """
    Load an instance of BEAM-DIMAP reader with single band SLC data
    """
    # Setup testing environment
    yield Sentinel1(metadata=data, product='GRD')


def test_important_metadata(dimap):
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

    expected = 'S1A_EW_GRDM_1SDH_20211221T075032_20211221T075104_041104_04E228_CED1_Orb_Cal_Spk'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_band_info(dimap):

    actual = dimap.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '10503'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(1, 'BAND_RASTER_WIDTH')
    expected = '10503'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_NAME')
    expected = 'Sigma0_HH'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_band_info(0, 'BAND_DESCRIPTION')
    expected = None
    assert actual == expected, assert_error(expected, actual)


def test_load_all_band_names(dimap):
    actual = dimap.get_band_info(None, 'BAND_NAME')
    expected = {'0': 'Sigma0_HH', '1': 'Sigma0_HV'}
    assert actual == expected, assert_error(expected, actual)


def test_abstracted_metadata(dimap):

    actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier')['text']
    expected = 'ESA Sentinel-1 IPF 003.40'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier')['desc']
    expected = 'Processing system identifier'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('incidence_near')['text']
    expected = '19.442898709420884'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_abstracted_metadata_attribute('PASS')['text']
    expected = 'DESCENDING'
    assert actual == expected, assert_error(expected, actual)


def test_processing_graph_with_attributes(dimap):

    actual = dimap.get_processing_history(0, 'operator')
    expected = 'Apply-Orbit-File'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(0, 'parameters')['orbitType']
    expected = 'Sentinel Precise (Auto Download)'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(2, 'parameters')['file']
    expected = r'C:\Users\Angelo\Documents\PANJI\Projects\beam-dimap-reader\S1A_EW_GRDM_1SDH_20211221T075032_20211221T075104_041104_04E228_CED1_Orb.dim'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(3, 'sources')['sourceProduct']
    expected = 'file:/C:/Users/Angelo/Documents/PANJI/Projects/beam-dimap-reader/S1A_EW_GRDM_1SDH_20211221T075032_20211221T075104_041104_04E228_CED1_Orb.dim'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.get_processing_history(4, 'operator')
    expected = 'Write'
    assert actual == expected, assert_error(expected, actual)


def testprocessing_graph_with_nonetypes(dimap):

    # Get list of operators
    actual = dimap.get_processing_history(None, 'operator')
    expected = {
        'node.0': 'Apply-Orbit-File',
        'node.1': 'Write',
        'node.2': 'Read',
        'node.3': 'Calibration',
        'node.4': 'Write',
        'node.5': 'Speckle-Filter',
        'node.6': 'Write'
    }
    assert actual == expected, assert_error(expected, actual)

    # Get all items in second node
    actual = dimap.get_processing_history(1, None)
    expected = {
        'node': 'node.1',
        'id': 'Write$17DEB67E923',
        'operator': 'Write',
        'moduleName': 'SNAP Graph Processing Framework (GPF)',
        'moduleVersion': '8.0.3',
        'purpose': 'Writes a data product to a file.',
        'authors': 'Marco Zuehlke, Norman Fomferra',
        'version': '1.3',
        'copyright': '(c) 2010 by Brockmann Consult',
        'processingTime': '2021-12-24T07:46:35.429Z',
        'sources': {'sourceProduct': 'file:/C:/Users/Angelo/Documents/PANJI/Projects/beam-dimap-reader/S1A_EW_GRDM_1SDH_20211221T075032_20211221T075104_041104_04E228_CED1_Orb.dim'},
        'parameters': {'writeEntireTileRows': 'true', 'file': 'C:\\Users\\Angelo\\Documents\\PANJI\\Projects\\beam-dimap-reader\\S1A_EW_GRDM_1SDH_20211221T075032_20211221T075104_041104_04E228_CED1_Orb.dim', 'deleteOutputOnFailure': 'true', 'formatName': 'BEAM-DIMAP', 'clearCacheAfterRowWrite': 'false'}}
    assert actual == expected, assert_error(expected, actual)
