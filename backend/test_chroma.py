import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="test_collection"
)

collection.add(
    ids=["doc1", "doc2"],
    documents=[
        "Retrieval-Augmented Generation uses external documents.",
        "A banana is a type of fruit."
    ]
)

results = collection.query(
    query_texts=["What does RAG use?"],
    n_results=2
)

print(results["documents"])