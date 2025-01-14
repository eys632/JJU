# 필요한 라이브러리 설치
# pip install -qU pypdf langchain_community pymupdf PyPDFium2 pdfminer.six

from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, PyPDFium2Loader, PDFMinerLoader, PDFMinerPDFasHTMLLoader

FILE_PATH = "./SPRI_AI_Brief_2023년12월호_F.pdf"

def show_metadata(docs):
    if docs:
        print("[metadata]")
        print(list(docs[0].metadata.keys()))
        print("\n[examples]")
        max_key_length = max(len(k) for k in docs[0].metadata.keys())
        for k, v in docs[0].metadata.items():
            print(f"{k:<{max_key_length}} : {v}")

def load_with_pypdf(file_path):
    """Load PDF with PyPDFLoader"""
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    show_metadata(docs)
    print("\n[content sample]")
    print(docs[0].page_content[:300])
    return docs

def load_with_pymupdf(file_path):
    """Load PDF with PyMuPDFLoader"""
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    show_metadata(docs)
    print("\n[content sample]")
    print(docs[0].page_content[:300])
    return docs

def load_with_pypdfium2(file_path):
    """Load PDF with PyPDFium2Loader"""
    loader = PyPDFium2Loader(file_path)
    docs = loader.load()
    show_metadata(docs)
    print("\n[content sample]")
    print(docs[0].page_content[:300])
    return docs

def load_with_pdfminer(file_path):
    """Load PDF with PDFMinerLoader"""
    loader = PDFMinerLoader(file_path)
    docs = loader.load()
    show_metadata(docs)
    print("\n[content sample]")
    print(docs[0].page_content[:300])
    return docs

def load_with_pdfminer_html(file_path):
    """Load PDF with PDFMinerPDFasHTMLLoader"""
    loader = PDFMinerPDFasHTMLLoader(file_path)
    docs = loader.load()
    show_metadata(docs)
    print("\n[content sample]")
    print(docs[0].page_content[:300])
    return docs

def main():
    print("\n--- PyPDFLoader ---\n")
    load_with_pypdf(FILE_PATH)

    print("\n--- PyMuPDFLoader ---\n")
    load_with_pymupdf(FILE_PATH)

    print("\n--- PyPDFium2Loader ---\n")
    load_with_pypdfium2(FILE_PATH)

    print("\n--- PDFMinerLoader ---\n")
    load_with_pdfminer(FILE_PATH)

    print("\n--- PDFMinerPDFasHTMLLoader ---\n")
    load_with_pdfminer_html(FILE_PATH)

if __name__ == "__main__":
    main()