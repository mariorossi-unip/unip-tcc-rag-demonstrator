from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Retrieval-Augmented Generation combines retrieval and language generation."
)

embedding = response.data[0].embedding

print("Embedding dimensions:", len(embedding))
print("First 10 values:")
print(embedding[:10])