import pymupdf
from pathlib import Path


def read_pdf(file_path):
    document = pymupdf.open(file_path)

    extracted_text = ""

    for page in document:

        page_text = page.get_text()

        extracted_text += page_text

    document.close()

    return extracted_text


if __name__ == "__main__":

    pdf_path = Path(__file__).parent / "documents" / "inventory_sop.pdf"

    text = read_pdf(pdf_path)

    print("EXTRACTED PDF CONTENT")
    print("-------------------------------")

    print(text)