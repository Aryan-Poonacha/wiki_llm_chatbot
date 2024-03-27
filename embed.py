import xml.etree.ElementTree as ET
import langchain as lc
import pinecone
import os

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Load XML data
tree = ET.parse('Data/yakuza_pages_current.xml')
root = tree.getroot()

# Convert XML data to a format usable by LangChain
data = lc.Data(root)

# Initialize LangChain
chain = lc.Chain()

# Ingest and embed data
embeddings = chain.ingest(data).embed()

# Initialize Pinecone
pc = pinecone.Pinecone(api_key='YOUR_API_KEY')
index = pc.Index('yakuza-wiki-index')

# Store embeddings in Pinecone
index.upsert(embeddings)