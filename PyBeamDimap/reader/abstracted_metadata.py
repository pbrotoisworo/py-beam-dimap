import re
# import xml.etree.ElementTree as ET

import pandas as pd


class AbstractedMetadata:

    def __init__(self, metadata, product):
        """
        Class for handling the abstracted metadata section of Sentinel-1 metadata

        :param metadata: ElementTree object containing parsed .dim data
        :param product: Sentinel-1 Product type
        """
        self._metadata = metadata
        self._target_xpath = './/MDElem[@name="Abstracted_Metadata"]'
        # Dataframe does not include nested elements in the abstracted metadata section
        self._dataframe = self._load_dataframe()
        self._product = product
        self._orbit_state_vectors = self._load_orbit_state_vectors()
        self._doppler_centroid_coeffs = self._load_doppler_centroid_coeffs()
        self._baselines = self._load_baselines()
        self._srgr_coeffs = self._load_srgr_coeffs()
        self._look_directions = self._load_look_direction_list()
        self._esd_measurement = EsdMeasurement(self._metadata, self._product)
        self._burst_boundary = self._load_burst_boundary()
        self._orbit_offsets = self._load_orbit_offsets()

    @property
    def dataframe(self) -> pd.DataFrame:
        """
        Dataframe object containing all non-nested abstracted metadata elements
        """
        return self._dataframe

    @property
    def burst_boundary(self):
        """
        Dataframe object containing burst boundary data
        """
        return self._burst_boundary

    @property
    def EsdMeasurement(self):
        """
        Subclass to handle ESD Measurement section. Access this property to access ESD measurement data.
        """
        return self._esd_measurement

    @property
    def orbit_state_vectors(self) -> pd.DataFrame:
        """
        Dataframe object containing orbit state vectors
        """
        return self._orbit_state_vectors

    @property
    def orbit_offsets(self) -> pd.DataFrame:
        """
        Dataframe object contaning orbit offsets
        """
        return self._orbit_offsets

    @property
    def srgr_coeffs(self) -> pd.DataFrame:
        """
        Dataframe object containing slant range to ground range (SRGR) coefficients
        """
        return self._srgr_coeffs

    @property
    def look_directions(self) -> pd.DataFrame:
        """
        Dataframe object containing look direction data
        """
        return self._look_directions

    @property
    def doppler_centroid_coeffs(self) -> pd.DataFrame:
        """
        Dataframe object containing doppler centroid coefficients
        """
        return self._doppler_centroid_coeffs

    @property
    def baselines(self) -> pd.DataFrame:
        """
        Dataframe object containing baseline data between two image acquisitions
        """
        return self._baselines

    def get_attribute(self, name, attribute_type='Value') -> str:
        """
        Load XML attribute from abstracted metadata section. Does not include nested sections.

        :param name: Element to search for in abstracted metadata
        :param attribute_type: Accepted attribute types are [Name, Value, Type, Description]
        """
        attr_type = attribute_type.title()
        output = self._dataframe[self._dataframe['Name'] == name][attr_type]

        if len(output) == 0:
            raise ValueError(f'Element "{name}" not found in abstracted metadata')

        output = list(output)[0]

        return output

    def _load_dataframe(self):
        name_list = []
        text_list = []
        type_list = []
        unit_list = []
        desc_list = []

        # Skip list contains nested abstracted metadata which needs to be extracted using other methods
        skip_list = ['Orbit_State_Vectors', 'SRGR_Coefficients', 'Doppler_Centroid_Coefficients',
                     'Doppler_Centroid_Coefficients', 'Baselines', 'ESD Measurement', 'Look_Direction_List',
                     'BurstBoundary', 'Orbit_Offsets', 'Product_Information']

        for item in list(self._metadata.findall(self._target_xpath)[0]):
            if item.attrib.get('name') in skip_list:
                continue
            name_list.append(item.attrib.get('name'))
            type_list.append(item.attrib.get('type'))
            unit_list.append(item.attrib.get('unit'))
            desc_list.append(item.attrib.get('desc'))
            # Clean \n character in item text
            if '\n' in item.text:
                text = None
            else:
                text = item.text
            text_list.append(text)

        data = {'Name': name_list, 'Value': text_list, 'Type': type_list, 'Description': desc_list}
        return pd.DataFrame(data)

    def _load_burst_boundary(self):
        elem = self._metadata.findall('.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="BurstBoundary"]/*')
        if len(elem) == 0:
            return

        burst_boundary_data = {}
        for swath in elem:

            for burst in swath:
                if burst.attrib['name'] == 'count':
                    continue
                col_name = f'{burst.attrib["name"]}_{swath.attrib["name"]}'
                if not burst_boundary_data.get(col_name):
                    burst_boundary_data[col_name] = {}

                for data in burst:
                    text = data.text
                    if '    ' in text:
                        text = None
                    burst_boundary_data[col_name][data.attrib['name']] = text
        return pd.DataFrame(burst_boundary_data)

    def _load_orbit_state_vectors(self, out_type_as_dataframe=True):
        elem = self._metadata.findall(f'{self._target_xpath}/MDElem[@name="Orbit_State_Vectors"]')[0]
        if len(elem) == 0:
            return

        vector = {}

        for vector_elem in list(elem):
            vector[vector_elem.attrib['name']] = {}
            vector_data = {}
            for item in vector_elem:
                vector_data[item.attrib['name']] = item.text
            vector[vector_elem.attrib['name']] = vector_data

        if out_type_as_dataframe is True:
            return pd.DataFrame(vector)
        else:
            return vector

    # Slant Range to Ground Range (SRGR)
    def _load_srgr_coeffs(self):
        elem = self._metadata.findall('.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="SRGR_Coefficients"]/*')
        if len(elem) == 0:
            return

        srgr_coeffs = []
        for idx in range(1, len(elem) + 1):
            coef_list = self._metadata.findall(
                f'.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="SRGR_Coefficients"]/MDElem[@name="srgr_coef_list.{idx}"]')

            for coef_data in coef_list:
                coef_dict = {}
                coef_dict['element'] = f'srgr_coef_list.{idx}'
                for item in coef_data:
                    if '    ' not in item.text:
                        coef_dict[item.attrib['name']] = item.text
                    else:
                        coef_dict['srgr_coef'] = list(item)[0].text
                srgr_coeffs.append(coef_dict)
        if not srgr_coeffs:
            return
        else:
            return pd.DataFrame(srgr_coeffs)

    def _load_doppler_centroid_coeffs(self, out_type_as_dataframe=True):
        elem = self._metadata.findall(f'{self._target_xpath}/MDElem[@name="Doppler_Centroid_Coefficients"]')[0]
        if len(elem) == 0:
            return

        coeffs = {}

        for coeff_elem in list(elem):
            coeffs_data = {}
            for coeff_list in coeff_elem:
                # Get nested coeffs
                if len(list(coeff_list)) == 0:
                    coeffs_data[coeff_list.attrib['name']] = coeff_list.text
                else:
                    for coeff_nest in coeff_list:
                        coeffs_data[coeff_list.attrib['name']] = coeff_nest.text
            coeffs[coeff_elem.attrib['name']] = coeffs_data

        if out_type_as_dataframe is True:
            return pd.DataFrame(coeffs)
        else:
            return coeffs

    def _load_baselines(self, out_type_as_dataframe=True):
        elem = self._metadata.findall(f'{self._target_xpath}/MDElem[@name="Baselines"]')
        if len(elem) == 0:
            return
        elem = elem[0]

        re_pattern = r'\d{2}...\d{4}'
        baselines = {}

        for reference in list(elem):
            reference_date = re.search(re_pattern, reference.attrib['name'])[0]

            # Loop through nested items
            for secondary in reference:
                secondary_date = re.search(re_pattern, secondary.attrib['name'])[0]
                if reference_date != secondary_date:
                    baseline_data = {x.attrib['name']: x.text for x in secondary}
                    baseline_data['Secondary Date'] = secondary_date
                    baselines[reference_date] = baseline_data

        if out_type_as_dataframe is True:
            return pd.DataFrame(baselines)
        else:
            return baselines

    def _load_look_direction_list(self):
        elem = self._metadata.findall('.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="Look_Direction_List"]/*')
        if len(elem) == 0:
            return

        look_direction_data = {}
        for item in elem:
            look_direction_data[item.attrib['name']] = {}
            for data in item:
                look_direction_data[item.attrib['name']][data.attrib['name']] = data.text

        return pd.DataFrame(look_direction_data)

    def _load_orbit_offsets(self):
        elem = self._metadata.findall('.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="Orbit_Offsets"]/*')
        if len(elem) == 0:
            return

        orbit_offsets = {}
        for ds in elem:
            orbit_offsets[ds.attrib['name']] = {}
            for data in ds:
                orbit_offsets[ds.attrib['name']][data.attrib['name']] = data.text

        return pd.DataFrame(orbit_offsets)


class EsdMeasurement:

    def __init__(self, metadata, product):
        """
        Class to handle ESD measurement properties in the abstracted metadata class
        """

        self._metadata = metadata
        self._product = product
        self._data = self._load_esd_measurement()
        if self._data is not None:
            self.images = [x for x in self._data.keys()]
        else:
            self.images = None
        self.parameters = self._metadata.findall(
                f'.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="ESD Measurement"]/*/*')
        if self.parameters is not None:
            self.parameters = [x.attrib['name'] for x in self.parameters]

    def dataframe(self, image=None, param=None, verbose=True):
        """
        Generate a Pandas dataframe of the ESD measurements. Only one image can be loaded at a time.

        :param image: Dataset to check. Default will use first image in the dimap file.
        :param param: Parameter to check. Default will use first parameter in the ESD measurement metadata
        """
        # Check if element exists
        elem = self._metadata.findall(
                f'.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="ESD Measurement"]/*/*')
        if len(elem) == 0:
            return

        if param is None:
            # Get first parameter as default
            param = self._metadata.findall(
                f'.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="ESD Measurement"]/*/*')[0].attrib['name']
        if image is None:
            # Get first image as default
            image = self.images[0]
        if verbose is True:
            print('ESD data for', image)
            print('Parameter is', param)

        data = self._data[image][param]
        df = pd.DataFrame(data)

        return df

    def _load_esd_measurement(self):
        elem = self._metadata.findall('.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="ESD Measurement"]/*')
        if len(elem) == 0:
            return

        image_list = []
        for image in list(elem):
            image_list.append(image.attrib['name'])

        esd_measurements = {}
        for image in image_list:
            elem = self._metadata.findall(f'.//MDElem[@name="Abstracted_Metadata"]/MDElem[@name="ESD Measurement"]/MDElem[@name="{image}"]/*')
            for param in elem:
                swath_data = {}
                for swath in param:
                    shift_data = {}
                    for data in swath:
                        shift_data[data.attrib['name']] = data.text
                    swath_data[swath.attrib['name']] = shift_data
            esd_measurements[image] = {param.attrib['name']: swath_data}

        return esd_measurements
