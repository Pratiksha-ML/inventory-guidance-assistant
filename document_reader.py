from pathlib import Path


def read_sop_document():

    file_path = Path("documents/inventory_sop.txt")

    with open(file_path, "r", encoding="utf-8") as file:

        document_text = file.read()

    return document_text


if __name__ == "__main__":

    content = read_sop_document()

    print("INVENTORY SOP DOCUMENT")
    print("-------------------------------")

    print(content)