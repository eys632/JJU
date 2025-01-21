
from langchain_community.document_loaders import PyPDFLoader as PyPDFLoaderClass
from langchain_community.document_loaders import PyMuPDFLoader as PyMuPDFLoaderClass
from langchain_community.document_loaders import PyPDFium2Loader as PyPDFium2LoaderClass
from langchain_community.document_loaders import PDFMinerLoader as PDFMinerLoaderClass
from langchain_community.document_loaders import PDFPlumberLoader as PDFPlumberLoaderClass

def load_with_pypdf(file_path):
    loader = PyPDFLoaderClass(file_path)
    docs = loader.load()
    return docs[0].page_content[:1000]

def load_with_pymupdf(file_path):
    loader = PyMuPDFLoaderClass(file_path)
    docs = loader.load()
    return docs[0].page_content[:1000]

def load_with_pypdfium(file_path):
    loader = PyPDFium2LoaderClass(file_path)
    docs = loader.load()
    return docs[0].page_content[:1000]

def load_with_pdfminer(file_path):
    loader = PDFMinerLoaderClass(file_path)
    docs = loader.load()
    return docs[0].page_content[:1000]

def load_with_pdfplumber(file_path):
    loader = PDFPlumberLoaderClass(file_path)
    docs = loader.load()
    return docs[0].page_content[:1000]
