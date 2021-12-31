import os

import pytest

# from PyBeamDimap.reader import BeamDimap
from PyBeamDimap.missions import Sentinel1

TEST_DIR = os.path.abspath('tests')
data2 = os.path.join(TEST_DIR, 'S1_IW_SLC_DInSARStack_20190902_20190914.dim')


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
    yield Sentinel1(metadata=data2, product='SLC')


def test_data2_important_metadata(dimap):
    """
    Test important metadata parameters
    """
    # Check extracted data is correct
    expected = 'DIMAP'
    assert dimap.metadata_format == expected, assert_error(expected, dimap.metadata_format)

    expected = '2.12.1'
    assert dimap.metadata_version == expected, assert_error(expected, dimap.metadata_version)

    expected = 'SENTINEL-1B'
    assert dimap.mission == expected, assert_error(expected, dimap.mission)

    expected = '20190902_20190914_DInSARStack'
    assert dimap.dataset_name == expected, assert_error(expected, dimap.dataset_name)


def test_data2_band_info(dimap):

    actual = dimap.ImageInterpretation.get_band_info(0, 'BAND_RASTER_WIDTH')
    expected = '5282'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(1, 'BAND_RASTER_WIDTH')
    expected = '5282'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(5, 'BAND_DESCRIPTION')
    expected = None
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(0, 'BAND_NAME')
    expected = 'Intensity_ifg_VV_02Sep2019_14Sep2019'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(1, 'BAND_NAME')
    expected = 'Intensity_ifg_VV_02Sep2019_14Sep2019_db'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(2, 'BAND_NAME')
    expected = 'Phase_ifg_VV_02Sep2019_14Sep2019'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(3, 'BAND_NAME')
    expected = 'coh_IW2_VV_02Sep2019_14Sep2019'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(4, 'BAND_NAME')
    expected = 'Unw_Phase_ifg_02Sep2019_14Sep2019_VV'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ImageInterpretation.get_band_info(5, 'BAND_NAME')
    expected = 'displacement_VV_slv1_02Sep2019'
    assert actual == expected, assert_error(expected, actual)


def test_data2_load_all_band_names(dimap):
    actual = dimap.ImageInterpretation.get_band_info(None, 'BAND_NAME')
    expected = {
        '0': 'Intensity_ifg_VV_02Sep2019_14Sep2019',
        '1': 'Intensity_ifg_VV_02Sep2019_14Sep2019_db',
        '2': 'Phase_ifg_VV_02Sep2019_14Sep2019',
        '3': 'coh_IW2_VV_02Sep2019_14Sep2019',
        '4': 'Unw_Phase_ifg_02Sep2019_14Sep2019_VV',
        '5': 'displacement_VV_slv1_02Sep2019'
    }
    assert actual == expected, assert_error(expected, actual)


def test_data2_get_abstracted_metadata(dimap):

    # actual = dimap.get_abstracted_metadata_attribute('Processing_system_identifier')['text']
    actual = dimap.AbstractedMetadata.get_attribute('Processing_system_identifier', 'Value')
    expected = 'ESA Sentinel-1 IPF 003.10'
    assert actual == expected, assert_error(expected, actual)

    # actual = dimap.get_abstracted_metadata_attribute('PRODUCT')['text']
    actual = dimap.AbstractedMetadata.get_attribute('PRODUCT', 'Value')
    expected = 'S1B_IW_SLC__1SDV_20190902T075741_20190902T075808_017856_0219A5_70FA'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.get_attribute('PASS', 'Value')
    expected = 'DESCENDING'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.get_attribute('centre_lat', 'Value')
    expected = '64.27210588794522'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.get_attribute('centre_lat', 'Type')
    expected = 'float64'
    assert actual == expected, assert_error(expected, actual)


def test_data2_abstracted_metadata_dataframe(dimap):

    # Test antenna_pointing value
    actual = dimap.AbstractedMetadata.dataframe
    actual = actual[actual['Name'] == 'antenna_pointing']['Value'].item()
    expected = 'right'
    assert actual == expected, assert_error(expected, actual)

    # Test PROC_TIME value
    actual = dimap.AbstractedMetadata.dataframe
    actual = actual[actual['Name'] == 'PROC_TIME']['Value'].item()
    expected = '02-SEP-2019 10:12:29.967601'
    assert actual == expected, assert_error(expected, actual)


def test_nested_abstracted_metadata_sections(dimap):

    # Orbit state vectors
    actual = dimap.AbstractedMetadata.orbit_state_vectors['orbit_vector1']['x_pos']
    expected = '3085342.723941803'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.orbit_state_vectors['orbit_vector2']['y_pos']
    expected = '-695560.9979515076'
    assert actual == expected, assert_error(expected, actual)

    # Doppler centroid coeffs
    actual = dimap.AbstractedMetadata.doppler_centroid_coeffs[dimap.AbstractedMetadata.doppler_centroid_coeffs.columns[0]]['coefficient.1']
    expected = '1.498285'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.doppler_centroid_coeffs[dimap.AbstractedMetadata.doppler_centroid_coeffs.columns[1]]['coefficient.2']
    expected = '-649.9965'
    assert actual == expected, assert_error(expected, actual)

    # Baselines
    actual = dimap.AbstractedMetadata.baselines[dimap.AbstractedMetadata.baselines.columns[0]]['Perp Baseline']
    expected = '10.542634010314941'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.AbstractedMetadata.baselines[dimap.AbstractedMetadata.baselines.columns[0]]['Modelled Coherence']
    expected = '0.9797642230987549'
    assert actual == expected, assert_error(expected, actual)

    # Orbit offsets
    actual = dimap.AbstractedMetadata.orbit_offsets.loc['init_offset_X']['init_offsets_slv1_02Sep2019']
    expected = '0'
    assert actual == expected, assert_error(expected, actual)

    # Look direction
    actual = dimap.AbstractedMetadata.look_directions.loc['head_lat']['look_direction1']
    expected = '64.26755881338691'
    assert actual == expected, assert_error(expected, actual)

    # ESD measurement
    actual = dimap.AbstractedMetadata.EsdMeasurement.dataframe(verbose=False).loc['azimuthShift']['IW2']
    expected = '0.0'
    assert actual == expected, assert_error(expected, actual)


def test_data2_processing_graph_with_attributes(dimap):

    actual = dimap.ProcessingGraph.get_processing_graph(0, 'operator')
    expected = 'Read'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(0, 'parameters')['copyMetadata']
    expected = 'true'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(4, 'parameters')['resamplingType']
    expected = 'BILINEAR_INTERPOLATION'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(5, 'operator')
    expected = 'Enhanced-Spectral-Diversity'
    assert actual == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(4, 'sources')

    expected = 'file:/E:/SAR_Iceland/sample/20190902_Orb.dim'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)
    expected = 'file:/E:/SAR_Iceland/sample/20190914_Orb.dim'
    assert actual['sourceProduct.1'] == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(1, 'sources')
    expected = 'file:/E:/SAR_Iceland/images/S1B_IW_SLC__1SDV_20190902T075741_20190902T075808_017856_0219A5_70FA.zip'
    assert actual['sourceProduct'] == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(17, 'sources')
    expected = 'file:/E:/SAR_Iceland/sample/20190902_20190914_Orb_Stack_Ifg_Deb_TopoPhase_ML_Flt_Unw_TC.dim'
    assert actual['sourceProduct.0'] == expected, assert_error(expected, actual)

    actual = dimap.ProcessingGraph.get_processing_graph(17, 'sources')
    expected = 'file:/E:/SAR_Iceland/sample/20190902_20190914_disp_TC.dim'
    assert actual['sourceProduct.1'] == expected, assert_error(expected, actual)


def test_data2_processing_graph_with_nonetypes(dimap):

    # Get list of operators
    actual = dimap.ProcessingGraph.get_processing_graph(None, 'operator')
    expected = {'node.0': 'Read', 'node.1': 'TOPSAR-Split', 'node.2': 'Apply-Orbit-File', 'node.3': 'Write',
                'node.4': 'Back-Geocoding', 'node.5': 'Enhanced-Spectral-Diversity', 'node.6': 'Write',
                'node.7': 'Read', 'node.8': 'Interferogram', 'node.9': 'TOPSAR-Deburst', 'node.10': 'TopoPhaseRemoval',
                'node.11': 'Multilook', 'node.12': 'GoldsteinPhaseFiltering', 'node.13': 'Read',
                'node.14': 'SnaphuImport', 'node.15': 'Terrain-Correction', 'node.16': 'Read', 'node.17': 'CreateStack'}
    assert actual == expected, assert_error(expected, actual)

    # Get all items in third node
    actual = dimap.ProcessingGraph.get_processing_graph(2, None)
    expected = {'node': 'node.2', 'id': 'Apply-Orbit-File (Initial)', 'operator': 'Apply-Orbit-File',
                'moduleName': 'S1TBX SAR Processing', 'moduleVersion': '8.0.3', 'purpose': 'Apply orbit file',
                'authors': 'Jun Lu, Luis Veci', 'version': '1.0',
                'copyright': 'Copyright (C) 2016 by Array Systems Computing Inc.',
                'processingTime': '2021-07-03T18:41:28.805Z',
                'sources': {'sourceProduct': 'product:S1B_IW_SLC__1SDV_20190902T075741_20190902T075808_017856_0219A5_70FA'},
                'parameters': {'orbitType': 'Sentinel Precise (Auto Download)', 'continueOnFail': 'true', 'polyDegree': '3'}}
    assert actual == expected, assert_error(expected, actual)
