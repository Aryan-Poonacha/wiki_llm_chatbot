import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

class PineconeSetup:
    def __init__(self):
        load_dotenv()
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.datafile_path = 'Data/yakuza_pages_current.xml'
        self.index_name = 'yakuza-wiki-index'

    def setup(self):
        # Convert XML data to a format usable by LangChain
        print("Converting XML data...")
        loader = UnstructuredXMLLoader(self.datafile_path)
        docs = loader.load()

        # Initialize Pinecone
        print("Initializing Pinecone...")
        pc = Pinecone(api_key=self.pinecone_api_key)
        index = pc.Index(self.index_name)

        # Initialize the embeddings model
        print("Initializing embeddings model...")
        embeddings_model = OpenAIEmbeddings(self.openai_api_key)

        # Generate the embeddings for the documents
        print("Generating embeddings...")
        embeddings = embeddings_model.embed_documents(docs)

        # Store embeddings in Pinecone
        print("Storing embeddings in Pinecone...")
        index.upsert([(doc.id, embedding) for doc, embedding in zip(docs, embeddings)])

        # Initialize the PineconeVectorStore with the documents and embeddings
        print("Initializing PineconeVectorStore...")
        docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=self.index_name)

        print("Done!")

# Usage
# pinecone_setup = PineconeSetup()
# pinecone_setup.setup()
