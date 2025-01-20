# src/loaders/excel_loader.py
from langchain_community.document_loaders import UnstructuredExcelLoader
from .document import Document

def load_excel(file_path: str) -> list[Document]:
    loader = UnstructuredExcelLoader(file_path)
    rows = loader.load()

    documents = []
    for row in rows:
        text = row.page_content
        meta = row.metadata
        meta["source"] = file_path
        documents.append(Document(content=text, metadata=meta))
    return documents
