# src/loaders/text_loader.py
from langchain_community.document_loaders import TextLoader
from .document import Document

def load_text(file_path: str) -> list[Document]:
    loader = TextLoader(file_path)
    docs = loader.load()

    documents = []
    for doc in docs:
        text = doc.page_content
        meta = doc.metadata
        meta["source"] = file_path
        documents.append(Document(content=text, metadata=meta))

    return documents
