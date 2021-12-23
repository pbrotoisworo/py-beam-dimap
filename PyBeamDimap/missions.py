from .reader import BeamDimap


class Sentinel1(BeamDimap):

    def __init__(self, metadata: str, product):
        """
        Read and extracty data from Sentinel-1 BEAM-DIMAP files (.dim)

        :param metadata: Path of .dim file
        :param product: Sentinel-1 product type [SLC, GRD, OCN]
        """
        super().__init__(metadata, 'SENTINEL-1')
        self.mission = self.metadata.findall(".//MDATTR[@name='MISSION']")[0].text
        self.product = f'Sentinel-1 {product}'

    def get_processing_history(self, node_index=None, attribute=None):
        """
        Access processing history metadata. When you process data in SNAP the software saves the operator, parameters,
        source data, and other relevant information. These data are saved in a list like object caleld a "node".
        They can be accessed by the processing order of the BEAM-DIMAP file. This method allows you to read specific
        operators and parameters used in your previous workflows.

        :param node_index: Index location of specific processing node. If None, then return all available nodes.
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the node.
        :return: List or dict object containing operator and parameter information
        """
        return self.get_processing_graph(node_index, attribute)

    def get_abstracted_metadata_attribute(self, name: str):
        """
        Load abstracted metadata section of the BEAM-DIMAP file. This data contains data that is usually related to the
        scene such as scan time, pass direction, and more.

        :param name: Name of the attribute to load
        :return: Object containing attribute information
        """

        target_elem = self.metadata.findall(f".//MDElem[@name='Abstracted_Metadata']/MDATTR[@name='{name}']")
        # Check if element exists
        if len(target_elem) == 0:
            raise ValueError(f'Could not find abstracted metadata value "{name}"!')

        target_elem = self.metadata.findall(f".//MDElem[@name='Abstracted_Metadata']/MDATTR[@name='{name}']")[0]
        attribute = target_elem.attrib
        attribute['text'] = target_elem.text
        return attribute

    def get_band_info(self, band_index=None, attribute=None):
        """
        Load metadata that is specific for loading band-specific data such as wavelength, band name, dimensions, and
        more.

        :param band_index: Load specific band using its band index. Default value None will load all bands
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the band.
        :return: Dict containing band specific information
        """
        return self._get_band_info(band_index, attribute)

    # TODO: Finish original metadata section
    # def get_original_metadata(self):
    #     return


class Sentinel2(BeamDimap):

    def __init__(self, metadata: str, product_type: str):
        """
        Read and extracty data from Sentinel-2 BEAM-DIMAP files (.dim)

        :param metadata: Path of .dim file
        :param product_type: Sentinel-2 product type [1C, 2A]
        """
        super().__init__(metadata, product_type)

        # Verify processing level is valid
        self._verify_product_type()

        self.mission = self._get_mission()
        self.product = f'Sentinel-2 {self._processing_level}'

    def _verify_product_type(self):
        valid = ['1C', '2A']
        if self._processing_level not in valid:
            raise ValueError(f'Processing level input "{self._processing_level}" not a valid processing level')

    def _get_mission(self):
        mission = self.metadata.findall(".//MDElem[@name='Datatake']/MDATTR[@name='SPACECRAFT_NAME']")
        if not mission:
            return
        else:
            return mission[0].text

    def get_processing_history(self, node_index=None, attribute=None):
        """
        Access processing history metadata. When you process data in SNAP the software saves the operator, parameters,
        source data, and other relevant information. These data are saved in a list like object caleld a "node".
        They can be accessed by the processing order of the BEAM-DIMAP file. This method allows you to read specific
        operators and parameters used in your previous workflows.

        :param node_index: Index location of specific processing node. If None, then return all available nodes.
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the node.
        :return: List or dict object containing operator and parameter information
        """
        return self.get_processing_graph(node_index, attribute)

    def get_band_info(self, band_index=None, attribute=None):
        """
        Load metadata that is specific for loading band-specific data such as wavelength, band name, dimensions, and
        more.

        :param band_index: Load specific band using its band index. Default value None will load all bands
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the band.
        :return: Dict containing band specific information
        """
        return self._get_band_info(band_index, attribute)


if __name__ == '__main__':
    pass
