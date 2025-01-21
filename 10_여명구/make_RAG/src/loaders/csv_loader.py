# src/loaders/csv_loader.py
from langchain_community.document_loaders import CSVLoader
from .document import Document

def load_csv(file_path: str) -> list[Document]:
    loader = CSVLoader(file_path)
    rows = loader.load()  # 각 행이 LangChain Document 형태

    documents = []
    for row in rows:
        text = row.page_content
        meta = row.metadata
        meta["source"] = file_path
        documents.append(Document(content=text, metadata=meta))

    return documents
