from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

# Initialize Pinecone
pinecone_api_key = os.getenv('PINECONE_API_KEY')  # Get Pinecone API key from environment variable
pc = Pinecone(api_key=pinecone_api_key)
index_name = 'yakuza-wiki-index'
index = pc.Index(index_name)

# Initialize the embeddings model
openai_api_key = os.getenv('OPENAI_API_KEY')  # Get Pinecone API key from environment variable
embeddings_model = OpenAIEmbeddings(openai_api_key)  # You may need to pass your OpenAI API key here

# Initialize the PineconeVectorStore
docsearch = PineconeVectorStore(index, embeddings_model, text_field="text")

# Query script
query = "your query here"  # Replace with your query
print(f"Query: {query}")
results = docsearch.similarity_search(query, k=10)  # Returns the ten most similar results

print("Results:")
for result in results:
    print(f"Document ID: {result.id}, Similarity Score: {result.score}")
