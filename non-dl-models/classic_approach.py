import os
import xml.etree.ElementTree as ET

class NaiveSearch:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def search(self, query):
        results = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.xml'):
                tree = ET.parse(os.path.join(self.data_dir, filename))
                root = tree.getroot()
                for elem in root.iter():
                    if query.lower() in elem.text.lower():
                        results.append(elem.text)
        return results

# Example usage:
# naive_search = NaiveSearch('path_to_your_data_directory')
# results = naive_search.search('your_search_query')
# print(results)
