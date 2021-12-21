import xmltodict


class BeamDimap:

    def __init__(self, metadata):
        """
        Class to handle BeamDimap parsing. This is intended for BEAM-DIMAP files only and not the raw ZIP files of
        the Sentinel satellites.

        :param metadata: Path of BEAM-DIMAP (.dim) file
        """
        # Load metadata
        with open(metadata) as f:
            self.metadata = xmltodict.parse(f.read())

        # Load BEAM-DIMAP XML sections
        self._abstracted_metadata = self._load_abstracted_metadata()
        self._band_info = self._load_image_interpretation()
        self._processing_history = self._load_processing_history()

        # Load important metadata
        self.metadata_format = self.metadata['Dimap_Document']['Metadata_Id']['METADATA_FORMAT']['#text']
        self.metadata_version = self.metadata['Dimap_Document']['Metadata_Id']['METADATA_FORMAT']['@version']
        self.product_description = self.get_abstracted_metadata_attribute('SPH_DESCRIPTOR')
        self.mission = self.get_abstracted_metadata_attribute('MISSION')
        self.dataset_name = self.metadata['Dimap_Document']['Dataset_Id']['DATASET_NAME']
        self.crs = self.metadata['Dimap_Document']['Coordinate_Reference_System']['WKT']

    def get_abstracted_metadata_attribute(self, name: str):
        """
        Load abstracted metadata section of the BEAM-DIMAP file. This data contains data that is usually related to the
        scene such as scan time, pass direction, and more.

        :param name: Name of the attribute to load
        :return: Object containing attribute information
        """
        for i, elem in enumerate(self._abstracted_metadata):
            if elem['@name'] == name:
                metadata = _XmlElement(dict(self._abstracted_metadata[i]), 'AbstractedMetadata')

                # In some cases it may not return a string type because there is additional nested data
                if not isinstance(metadata, str):
                    return metadata.text
                else:
                    return metadata

        raise ValueError(f'Attribute "{name}" not found in abstracted metadata!')

    def get_band_info(self, band_index=None, attribute=None):
        """
        Load metadata that is specific for loading band-specific data such as wavelength, band name, dimensions, and
        more.

        :param band_index: Load specific band using its band index. Default value None will load all bands
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the band.
        :return: Dict containing band specific information
        """
        band_count = len(self._band_info) - 1

        # Load all bands by default
        if band_index is None:
            if attribute is None:
                return self._band_info
            else:
                target_elem = {}
                for item in self._band_info:
                    target_elem[item['BAND_INDEX']] = item[attribute]
                return target_elem
        # Load specific band
        else:
            if band_index > band_count:
                raise IndexError(
                    f'User inputted band index "{band_index}" is greater than maximum index "{band_count}"')
            if attribute is None:
                return self._band_info[band_index]
            else:
                return self._band_info[band_index][attribute]

    def get_processing_history(self, node_index=None, attribute=None):
        """
        Access processing history metadata. When you process data in SNAP the software saves the operator, parameters,
        source data, and other relevant information. These data are saved in a list like object caleld a "node".
        They can be accessed by the processing order of the BEAM-DIMAP file. This method allows you to read specific
        operators and parameters used in your previous workflows.

        :param node_index: Index location of specific processing node. If None, then return entire processing
            history.
        :param attribute: Name of specific attribute to load. If None then it will load all attributes for the node.
        :return: List or dict object containing operator and parameter information
        """
        if node_index is None:
            if attribute is None:
                return self._processing_history
            else:
                target_elem = {}
                for item in self._processing_history:
                    target_elem[item['node']] = item[attribute]
                return target_elem
        else:
            if attribute is None:
                # Get all class objects in dictionary format
                cls_dict = vars(_XmlElement(self._processing_history[node_index], section='processing'))['_elements']
                return cls_dict
            else:
                return _XmlElement(self._processing_history[node_index], section='processing')[attribute]

    def _load_image_interpretation(self):
        """
        Load image interpretation section
        """
        bands = self.metadata['Dimap_Document']['Image_Interpretation']['Spectral_Band_Info']
        band_metadata = []

        for elem in bands:

            # Get target elem. The element structure changes slightly depending if multiband or singleband
            if isinstance(elem, str):
                # Single band
                target_elem = bands
                band_path = self.metadata['Dimap_Document']['Data_Access']['Data_File']['DATA_FILE_PATH']['@href']

            else:
                # Multiband
                target_elem = elem
                band_index = target_elem.get('BAND_INDEX')
                band_path = self.metadata['Dimap_Document']['Data_Access']['Data_File'][int(band_index)][
                    'DATA_FILE_PATH']['@href']

            band_metadata.append({
                'BAND_INDEX': target_elem.get('BAND_INDEX'),
                'BAND_PATH': band_path,
                'BAND_DESCRIPTION': target_elem.get('BAND_DESCRIPTION'),
                'BAND_NAME': target_elem.get('BAND_NAME'),
                'BAND_RASTER_WIDTH': target_elem.get('BAND_RASTER_WIDTH'),
                'BAND_RASTER_HEIGHT': target_elem.get('BAND_RASTER_HEIGHT'),
                'DATA_TYPE': target_elem.get('DATA_TYPE'),
                'BAND_WAVELEN': target_elem.get('BAND_WAVELEN'),
                'BANDWIDTH': target_elem.get('BANDWIDTH'),
                'SCALING_FACTOR': target_elem.get('SCALING_FACTOR'),
                'SCALING_OFFSET': target_elem.get('SCALING_OFFSET'),
                'LOG10_SCALED': target_elem.get('LOG10_SCALED'),
                'NO_DATA_VALUE_USED': target_elem.get('NO_DATA_VALUE_USED'),
                'NO_DATA_VALUE': target_elem.get('NO_DATA_VALUE'),
                'VALID_MASK_TERM': target_elem.get('VALID_MASK_TERM'),
                'IMAGE_TO_MODEL_TRANSFORM': target_elem.get('IMAGE_TO_MODEL_TRANSFORM')
            })
        return band_metadata

    def _load_abstracted_metadata(self):
        """
        Load abstracted metadata section
        """
        return self.metadata['Dimap_Document']['Dataset_Sources']['MDElem']['MDElem'][0]['MDATTR']

    # TODO: Finish original metadata section
    # def get_original_metadata(self):
    #     return

    def _load_processing_history(self):
        """
        Load graph processing history section
        """
        # Load processing graph
        target_elem = None
        for idx, elem in enumerate(self.metadata['Dimap_Document']['Dataset_Sources']['MDElem']['MDElem']):
            if elem['@name'] == 'Processing_Graph':
                target_elem = self.metadata['Dimap_Document']['Dataset_Sources']['MDElem']['MDElem'][idx]['MDElem']
                break

        # Loop through nodes
        history = []
        for elem in target_elem:

            # Get parameter history
            parameters = {}
            try:
                for item in elem['MDElem'][1]['MDATTR']:
                    parameters[item['@name']] = item['#text']
            except (KeyError, TypeError):
                parameters = None

            # Get processing time
            try:
                processing_time = elem['MDATTR'][8]['#text']
            except IndexError:
                processing_time = None

            # Get sources
            sources = {}
            # print(elem['@name'], elem['MDATTR'][1]['#text'])
            target_source_elem = dict(elem['MDElem'][0].items())
            if target_source_elem.get('MDATTR') is None:
                sources = None
            else:
                target_source_elem = target_source_elem['MDATTR']#['#text']
                if isinstance(target_source_elem, list):
                    for item in target_source_elem:
                        sources[item['@name']] = item['#text']
                else:
                    sources[target_source_elem['@name']] = target_source_elem['#text']

            history_dict = {
                'node': elem['@name'],
                'operator': elem['MDATTR'][1]['#text'],
                'moduleName': elem['MDATTR'][2]['#text'],
                'moduleVersion': elem['MDATTR'][3]['#text'],
                'purpose': elem['MDATTR'][4]['#text'],
                'authors': elem['MDATTR'][5]['#text'],
                'version': elem['MDATTR'][6]['#text'],
                'copyright': elem['MDATTR'][7]['#text'],
                'processingTime': processing_time,
                'sources': sources,
                'parameters': parameters
            }

            history.append(history_dict)
        return history


class _XmlElement:

    def __init__(self, node: dict, section: str):
        """
        Dynamically create class based on dictionary object
        :param node: Dictionary containing node data
        """

        self._elements = {}
        for key, value in node.items():
            if section == 'processing':
                pass
            if section == 'AbstractedMetadata':
                key = key[1:]
            self._elements[key] = value
            setattr(_XmlElement, key, value)

    def __getitem__(self, item):
        if item not in self._elements.keys():
            raise ValueError(f'Attribute "{item}" does not exist in this section.')
        return self._elements[item]


if __name__ == '__main__':
    dimap = BeamDimap(r'C:\Users\Angelo\Documents\PANJI\Projects\beam-dimap-reader\tests\S1_coherance.dim')
    print(dimap.get_processing_history(None, 'operator'))
    print(dimap.get_band_info(None, 'BAND_NAME'))
    pass
