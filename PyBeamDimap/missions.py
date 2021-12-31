from PyBeamDimap.reader.core import BeamDimap

from .reader.abstracted_metadata import AbstractedMetadata
from .reader.processing_graph import ProcessingGraph
from .reader.core import ImageInterpretation


class Sentinel1(BeamDimap):

    def __init__(self, metadata: str, product):
        """
        Read and extracty data from Sentinel-1 BEAM-DIMAP files (.dim)

        :param metadata: Path of .dim file
        :param product: Sentinel-1 product type [SLC, GRD, OCN]
        """
        super().__init__(metadata, 'SENTINEL-1')
        self.mission = self._metadata.findall(".//MDATTR[@name='MISSION']")[0].text

        # Abstracted metadata sections
        self.AbstractedMetadata = AbstractedMetadata(self._metadata, product)
        self.ProcessingGraph = ProcessingGraph(self._metadata, product)
        self.ImageInterpretation = ImageInterpretation(self._metadata)


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
        self.ProcessingGraph = ProcessingGraph(self._metadata, product_type)

    def _verify_product_type(self):
        valid = ['1C', '2A']
        if self._processing_level not in valid:
            raise ValueError(f'Processing level input "{self._processing_level}" not a valid processing level')

    def _get_mission(self):
        mission = self._metadata.findall(".//MDElem[@name='Datatake']/MDATTR[@name='SPACECRAFT_NAME']")
        if not mission:
            return
        else:
            return mission[0].text


if __name__ == '__main__':
    pass
