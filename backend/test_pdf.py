import fitz

pdf_path = "./data/papers/lewis_2020_rag.pdf"

document = fitz.open(pdf_path)

print("Pages:", len(document))

for page_number, page in enumerate(document):
    text = page.get_text()

    print(f"\n--- PAGE {page_number + 1} ---")
    print(text[:500])