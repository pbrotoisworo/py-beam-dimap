# Reader file handles all functions related to reading and parsing BEAM-DIMAP files
import xml.etree.ElementTree as ET

from .abstracted_metadata import AbstractedMetadata


class BeamDimap:

    def __init__(self, metadata: str, processing_level: str):
        """
        Class that handles BEAM-DIMAP data that is present in all missions. This is intended for BEAM-DIMAP files only
        and not the raw ZIP files of the Sentinel satellites. This is meant to be subclassed by the Sentinel classes in
        missions.py

        :param metadata: Path of BEAM-DIMAP (.dim) file
        """
        # Load metadata
        tree = ET.parse(metadata)
        self._metadata = tree.getroot()

        self._processing_level = processing_level

        # Load BEAM-DIMAP XML sections
        self.ImageInterpretation = ImageInterpretation(self._metadata)

        # Load universal metadata
        self.metadata_format = self._metadata.findall('.//METADATA_FORMAT')[0].text
        self.metadata_version = self._metadata.findall('.//METADATA_FORMAT')[0].attrib['version']
        self.dataset_name = self._metadata.findall('.//DATASET_NAME')[0].text
        self.crs = self._get_crs()

    def _get_crs(self):
        crs = self._metadata.findall('.//Coordinate_Reference_System/WKT')
        if not crs:
            return None
        else:
            return crs[0].text


class ImageInterpretation:

    def __init__(self, metadata):
        """
        Class that handles ImageInterpretation section of BEAM-DIMAP files

        :param metadata: Parsed metadata file
        """
        self._metadata = metadata
        self._bands_data = self._load_image_interpretation()

    @property
    def band_data(self) -> list:
        """
        List containing metadata for all available bands
        """
        return self._bands_data

    def _load_image_interpretation(self):
        bands = self._metadata.findall('.//Image_Interpretation/Spectral_Band_Info')
        bands_children = [list(x) for x in bands]
        bands_list = []
        for child in bands_children:
            bands_dict = {}
            for grandchild in child:
                bands_dict[grandchild.tag] = grandchild.text
            bands_list.append(bands_dict)
        return bands_list

    def get_band_info(self, band_index=None, attribute=None):
        """
        Load metadata that is specific for loading band-specific data such as wavelength, band name, dimensions, and
        more.

        :param band_index: Load specific band using its band index. Default value None will load all bands
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the band.
        :return: Dict containing band specific information
        """
        # Get spectral bands element
        band_element = self._metadata.findall('.//Image_Interpretation/Spectral_Band_Info')

        # Load elements
        band_list = []
        for idx in range(len(band_element)):
            # Loop through band indices
            band_elem = self._metadata.findall(f".//Image_Interpretation/Spectral_Band_Info[BAND_INDEX='{idx}']")[0]
            band_data = {}
            for band in band_elem:
                band_data[band.tag] = band.text
            band_list.append(band_data)

        if band_index is None:
            if attribute is None:
                return band_list
            else:
                output_bands = {}
                for band in band_list:
                    output_bands[band['BAND_INDEX']] = band[attribute]
                return output_bands
        else:
            if attribute is None:
                return band_list[band_index]
            else:
                return band_list[band_index][attribute]


if __name__ == '__main__':
    pass
