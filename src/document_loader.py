from typing import List

from langchain_core.documents import Document
from pypdf import PdfReader


def load_pdf(uploaded_file) -> List[Document]:
    """
    Read an uploaded PDF and return one Document per page.
    """

    pdf_reader = PdfReader(uploaded_file)
    documents: List[Document] = []

    for page_number, page in enumerate(
        pdf_reader.pages,
        start=1,
    ):
        page_text = page.extract_text()

        if not page_text or not page_text.strip():
            continue

        document = Document(
            page_content=page_text,
            metadata={
                "source": uploaded_file.name,
                "page": page_number,
            },
        )

        documents.append(document)

    return documents