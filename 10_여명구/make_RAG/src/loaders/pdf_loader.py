# src/loaders/pdf_loader.py
from langchain_community.document_loaders import PyPDFLoader
from .document import Document

def load_pdf(file_path: str) -> list[Document]:
    """
    PDF 파일에서 텍스트를 추출해 Document 리스트 반환.
    """
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()  # 페이지 단위로 분할

    documents = []
    for i, page in enumerate(pages):
        text = page.page_content
        meta = {"source": file_path, "page": i+1}
        documents.append(Document(content=text, metadata=meta))
    return documents
