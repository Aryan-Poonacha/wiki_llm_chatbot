import os
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

datafile_path = 'Data/yakuza_pages_current.xml'
test_path = 'Data/test.xml'

# Convert XML data to a format usable by LangChain
print("Converting XML data...")
loader = UnstructuredXMLLoader(test_path)
docs = loader.load()

# Initialize Pinecone
print("Initializing Pinecone...")
pinecone_api_key = os.getenv('PINECONE_API_KEY')  # Get Pinecone API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')  # Get Pinecone API key from environment variable
pc = Pinecone(api_key=pinecone_api_key)
index_name = 'yakuza-wiki-index'
index = pc.Index(index_name)

# Initialize the embeddings model
print("Initializing embeddings model...")
embeddings_model = OpenAIEmbeddings(openai_api_key)  # You may need to pass your OpenAI API key here

# Generate the embeddings for the documents
print("Generating embeddings...")
embeddings = embeddings_model.embed_documents(docs)

# Store embeddings in Pinecone
print("Storing embeddings in Pinecone...")
index.upsert([(doc.id, embedding) for doc, embedding in zip(docs, embeddings)])

# Initialize the PineconeVectorStore with the documents and embeddings
print("Initializing PineconeVectorStore...")
docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

print("Done!")
