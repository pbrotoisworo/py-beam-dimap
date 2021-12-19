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
        self.product_description = self.get_abstracted_metadata_attribute('SPH_DESCRIPTOR').text
        self.mission = self.get_abstracted_metadata_attribute('MISSION').text
        self.dataset_name = self.metadata['Dimap_Document']['Dataset_Id']['DATASET_NAME']
        self.crs = self.metadata['Dimap_Document']['Coordinate_Reference_System']['WKT']

    def get_abstracted_metadata_attribute(self, name: str):
        for i, elem in enumerate(self._abstracted_metadata):
            if elem['@name'] == name:
                return _DictToClassObject(dict(self._abstracted_metadata[i]), 'AbstractedMetadata')
        return

    def get_band_info(self, band_index=None):

        band_count = len(self._band_info) - 1

        # Load all bands by default
        if band_index is None:
            return self._band_info
        else:
            if band_index > band_count:
                raise IndexError(
                    f'User inputted band index "{band_index}" is greater than maximum index "{band_count}"')
            return self._band_info[band_index]
            # return _DictKeyToClassObject(self._band_info[band_index])

    def get_processing_history(self, node_index=None):
        if node_index is None:
            return self._processing_history
        else:
            return _DictToClassObject(self._processing_history[node_index], section='processing')

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
    def load_original_metadata(self):
        return

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
                 'purpose': elem['MDATTR'][4]['#text'],
                 'processingTime': processing_time,
                 'sources': sources,
                 'parameters': parameters
            }

            history.append(history_dict)
        return history


class _DictToClassObject:

    def __init__(self, node: dict, section: str):
        """
        Dynamically create class based on dictionary object
        :param node: Dictionary containing node data
        """
        for key, value in node.items():
            if section == 'processing':
                pass
            if section == 'AbstractedMetadata':
                key = key[1:]
            setattr(_DictToClassObject, key, value)


if __name__ == '__main__':
    pass
