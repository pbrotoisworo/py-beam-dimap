# Reader file handles all functions related to reading and parsing BEAM-DIMAP files
import xml.etree.ElementTree as ET


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
        self.metadata = tree.getroot()

        self._processing_level = processing_level

        # Load BEAM-DIMAP XML sections
        self._band_info = self._load_image_interpretation()

        # Load universal metadata
        self.metadata_format = self.metadata.findall('.//METADATA_FORMAT')[0].text
        self.metadata_version = self.metadata.findall('.//METADATA_FORMAT')[0].attrib['version']
        self.dataset_name = self.metadata.findall('.//DATASET_NAME')[0].text
        self.crs = self._get_crs()

    def _get_crs(self):
        crs = self.metadata.findall('.//Coordinate_Reference_System/WKT')
        if not crs:
            return None
        else:
            return crs[0].text

    def _load_image_interpretation(self):
        bands = self.metadata.findall('.//Image_Interpretation/Spectral_Band_Info')
        bands_children = [list(x) for x in bands]
        bands_list = []
        for child in bands_children:
            bands_dict = {}
            for grandchild in child:
                bands_dict[grandchild.tag] = grandchild.text
            bands_list.append(bands_dict)
        return bands_list

    def _get_band_info(self, band_index=None, attribute=None):
        """
        Load metadata that is specific for loading band-specific data such as wavelength, band name, dimensions, and
        more.

        :param band_index: Load specific band using its band index. Default value None will load all bands
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the band.
        :return: Dict containing band specific information
        """
        # Get spectral bands element
        band_element = self.metadata.findall('.//Image_Interpretation/Spectral_Band_Info')

        # Load elements
        band_list = []
        for idx in range(len(band_element)):
            # Loop through band indices
            band_elem = self.metadata.findall(f".//Image_Interpretation/Spectral_Band_Info[BAND_INDEX='{idx}']")[0]
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

    def get_processing_graph(self, node_index=None, attribute=None):

        # Get parameters
        node_list = []
        # Loop through nodes
        for idx, child in enumerate(self.metadata.findall(".//MDElem[@name='Processing_Graph']/*")):
            node_data = {'node': f'node.{idx}'}
            # Loop through elements in each node
            for grandchild in list(child):
                if grandchild.text is not None:
                    if grandchild.text.rstrip():
                        node_data[grandchild.attrib['name']] = grandchild.text.rstrip()

            # Get sources
            sources = self.metadata.findall(f".//MDElem[@name='node.{idx}']/MDElem[@name='sources']/*")
            if not sources:
                sources_dict = None
            else:
                sources_dict = {}
                for source in sources:
                    sources_dict[source.attrib['name']] = source.text
                # sources_list.append(sources_dict)
            node_data['sources'] = sources_dict

            # parameters_list = []
            param_elem = self.metadata.findall(
                f".//MDElem[@name='Processing_Graph']/MDElem[@name='node.{idx}']/MDElem[@name='parameters']/*")
            # Save parameters in node
            node_parameters = {}
            for param in param_elem:
                node_parameters[param.attrib['name']] = param.text
            # parameters_list.append(node_parameters)
            node_data['parameters'] = node_parameters
            # print(node_data)
            node_list.append(node_data)

        if node_index is None:
            if attribute is None:
                return node_list
            else:
                output_dict = {}
                for node in node_list:
                    output_dict[node['node']] = node[attribute]
                return output_dict

        else:
            if attribute is None:
                return node_list[node_index]
            else:
                return node_list[node_index][attribute]


if __name__ == '__main__':
    pass
