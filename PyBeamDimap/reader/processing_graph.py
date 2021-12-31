class ProcessingGraph:

    def __init__(self, metadata, product):
        self._metadata = metadata
        self._product = product

    def get_processing_graph(self, node_index=None, attribute=None):

        # Get parameters
        node_list = []
        # Loop through nodes
        for idx, child in enumerate(self._metadata.findall(".//MDElem[@name='Processing_Graph']/*")):
            node_data = {'node': f'node.{idx}'}
            # Loop through elements in each node
            for grandchild in list(child):
                if grandchild.text is not None:
                    if grandchild.text.rstrip():
                        node_data[grandchild.attrib['name']] = grandchild.text.rstrip()

            # Get sources
            sources = self._metadata.findall(f".//MDElem[@name='node.{idx}']/MDElem[@name='sources']/*")
            if not sources:
                sources_dict = None
            else:
                sources_dict = {}
                for source in sources:
                    sources_dict[source.attrib['name']] = source.text
            node_data['sources'] = sources_dict

            param_elem = self._metadata.findall(
                f".//MDElem[@name='Processing_Graph']/MDElem[@name='node.{idx}']/MDElem[@name='parameters']/*")
            # Save parameters in node
            node_parameters = {}
            for param in param_elem:
                node_parameters[param.attrib['name']] = param.text
            node_data['parameters'] = node_parameters
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
