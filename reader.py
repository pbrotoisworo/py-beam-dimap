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
        for i, elem in enumerate(self._abstracted_metadata):
            if elem['@name'] == name:
                return dict(self._abstracted_metadata[i])
        return

    def get_band_info(self, band_index=None):

        band_count = len(self._band_info) - 1

        # Load all bands by default
        if band_index is None:
            return self._band_info
        else:
            if band_index > band_count:
                raise IndexError(f'User inputted band index "{band_index}" is greater than maximum index "{band_count}"')
            return self._band_info[band_index]

    def get_processing_history(self, node_index=None):

        if node_index is None:
            return self._processing_history
        else:
            return self._processing_history[node_index]

    def _load_image_interpretation(self):
        """
        Load image interpretation section
        """
        bands = self.metadata['Dimap_Document']['Image_Interpretation']['Spectral_Band_Info']
        band_metadata = []

        for elem in bands:
            band_metadata.append({
                'band_index': elem.get('BAND_INDEX'),
                'band_path':
                    self.metadata['Dimap_Document']['Data_Access']['Data_File'][int(elem.get('BAND_INDEX'))][
                        'DATA_FILE_PATH']['@href'],
                'band_description': elem.get('BAND_DESCRIPTION'),
                'band_name': elem.get('BAND_NAME'),
                'band_raster_width': elem.get('BAND_RASTER_WIDTH'),
                'band_raster_height': elem.get('BAND_RASTER_HEIGHT'),
                'data_type': elem.get('DATA_TYPE'),
                'band_wavelen': elem.get('BAND_WAVELEN'),
                'bandwidth': elem.get('BANDWIDTH'),
                'scaling_factor': elem.get('SCALING_FACTOR'),
                'scaling_offset': elem.get('SCALING_OFFSET'),
                'log10_scaled': elem.get('LOG10_SCALED'),
                'no_data_value_used': elem.get('NO_DATA_VALUE_USED'),
                'no_data_value': elem.get('NO_DATA_VALUE'),
                'valid_mask_term': elem.get('VALID_MASK_TERM'),
                'image_to_model_transform': elem.get('IMAGE_TO_MODEL_TRANSFORM')
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

            history.append(
                {'node': elem['@name'],
                 'operator': elem['MDATTR'][1]['#text'],
                 'parameters': parameters}
            )

        return history


if __name__ == '__main__':
    pass
