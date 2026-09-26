from dotenv import load_dotenv

from .embeddings import create_embedding
from .vector_store import get_collection


load_dotenv()


def search_documents(query: str, n_results: int = 5) -> list[dict]:
    """
    Performs semantic search against the document collection.

    Returns the most relevant document chunks for the query.
    """

    collection = get_collection()

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    search_results = []

    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances
    ):
        search_results.append(
            {
                "id": chunk_id,
                "text": document,
                "metadata": metadata,
                "distance": distance
            }
        )

    return search_results


def main():

    query = input("\nAsk a question: ")

    results = search_documents(query)

    print("\n==============================")
    print("SEARCH RESULTS")
    print("==============================")

    for index, result in enumerate(results, start=1):

        metadata = result["metadata"]

        print(f"\n--- RESULT {index} ---")

        print(f"Source: {metadata.get('source')}")
        print(f"Page: {metadata.get('page')}")
        print(f"Chunk: {metadata.get('chunk_index')}")
        print(f"Distance: {result['distance']:.4f}")

        print("\nText:")
        print(result["text"][:1000])
        print()


if __name__ == "__main__":
    main()