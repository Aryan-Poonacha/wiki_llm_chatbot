import os
import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDFSearch:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.documents = []
        self.vectorizer = TfidfVectorizer()

        # Load documents
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.xml'):
                tree = ET.parse(os.path.join(self.data_dir, filename))
                root = tree.getroot()
                for elem in root.iter():
                    self.documents.append(elem.text)

        # Compute TF-IDF
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def search(self, query):
        query_vector = self.vectorizer.transform([query])
        cosine_similarities = (self.tfidf_matrix * query_vector.T).toarray().ravel()
        relevant_indices = cosine_similarities.argsort()[:-6:-1]
        return [self.documents[i] for i in relevant_indices]

# Example usage:
# tfidf_search = TFIDFSearch('path_to_your_data_directory')
# results = tfidf_search.search('your_search_query')
# print(results)
