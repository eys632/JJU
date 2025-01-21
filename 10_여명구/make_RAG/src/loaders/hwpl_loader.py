# src/loaders/hwpl_loader.py
from langchain_teddynote.document_loaders import HWPLoader
from .document import Document

def load_hwp(file_path: str) -> list[Document]:
    loader = HWPLoader(file_path)
    docs = loader.load()

    documents = []
    for doc in docs:
        text = doc.page_content
        meta = doc.metadata
        meta["source"] = file_path
        documents.append(Document(content=text, metadata=meta))

    return documents
