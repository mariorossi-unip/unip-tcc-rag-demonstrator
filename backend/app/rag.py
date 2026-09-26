from .search import search_documents
from .llm import generate_answer


def build_context(results: list[dict]) -> str:
    """
    Converts retrieved search results into the context
    that will be provided to the language model.
    """

    context_parts = []

    for index, result in enumerate(results, start=1):

        metadata = result["metadata"]

        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")
        chunk = metadata.get("chunk_index", "Unknown")

        context_parts.append(
            f"""
[Document {index}]
Source: {source}
Page: {page}
Chunk: {chunk}

{result["text"]}
"""
        )

    return "\n".join(context_parts)


def ask_rag(
    question: str,
    n_results: int = 5
) -> dict:
    """
    Executes the complete RAG pipeline.
    """

    results = search_documents(
        query=question,
        n_results=n_results
    )

    context = build_context(results)

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "results": results,
        "context": context
    }


if __name__ == "__main__":

    question = input("\nAsk a question: ")

    result = ask_rag(question)

    print("\n==============================")
    print("ANSWER")
    print("==============================")

    print(result["answer"])

    print("\n==============================")
    print("RETRIEVED DOCUMENTS")
    print("==============================")

    for index, item in enumerate(
        result["results"],
        start=1
    ):

        metadata = item["metadata"]

        print(
            f"\n{index}. "
            f"{metadata.get('source')} "
            f"(page {metadata.get('page')}, "
            f"chunk {metadata.get('chunk_index')})"
        )

        print(
            f"Distance: {item['distance']:.4f}"
        )

    print("\n==============================")
    print("CONTEXT SENT TO LLM")
    print("==============================")

    print(result["context"])