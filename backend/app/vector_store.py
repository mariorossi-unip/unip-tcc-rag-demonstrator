import chromadb


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "rag_documents"


def get_collection():

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection