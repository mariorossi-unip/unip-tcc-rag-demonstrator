import os
import sys
import fitz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.embeddings import create_embedding
from app.vector_store import get_collection


PAPERS_DIRECTORY = "./data/papers"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_text(text: str) -> list[str]:

    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_pdf(pdf_path: str):

    collection = get_collection()

    filename = os.path.basename(pdf_path)

    print(f"\nProcessing: {filename}")

    document = fitz.open(pdf_path)

    total_chunks = 0

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        if not text.strip():
            continue

        chunks = split_text(text)

        for chunk_index, chunk in enumerate(chunks):

            chunk_id = (
                f"{filename}"
                f"_page_{page_number}"
                f"_chunk_{chunk_index}"
            )

            print(
                f"Embedding {filename} | "
                f"page {page_number} | "
                f"chunk {chunk_index}"
            )

            embedding = create_embedding(chunk)

            collection.upsert(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[
                    {
                        "source": filename,
                        "page": page_number,
                        "chunk_index": chunk_index
                    }
                ]
            )

            total_chunks += 1

    print(
        f"Finished {filename}: "
        f"{total_chunks} chunks stored."
    )


def ingest_all_pdfs():

    pdf_files = [
        filename
        for filename in os.listdir(PAPERS_DIRECTORY)
        if filename.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("No PDF files found.")
        return

    for filename in pdf_files:

        pdf_path = os.path.join(
            PAPERS_DIRECTORY,
            filename
        )

        ingest_pdf(pdf_path)


if __name__ == "__main__":
    ingest_all_pdfs()