# src/loaders/web_loader.py
from langchain_community.document_loaders import WebBaseLoader
from .document import Document

def load_web(url: str) -> list[Document]:
    loader = WebBaseLoader(url)
    docs = loader.load()

    documents = []
    for doc in docs:
        text = doc.page_content
        meta = doc.metadata
        meta["source"] = url
        documents.append(Document(content=text, metadata=meta))

    return documents
