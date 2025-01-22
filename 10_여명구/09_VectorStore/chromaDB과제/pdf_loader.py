from langchain_community.document_loaders import (
    PyPDFLoader,
    PyMuPDFLoader,
    PyPDFium2Loader,
    PDFMinerLoader,
    PDFMinerPDFasHTMLLoader,
)
import os

# PDF 파일 경로 설정
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"10_여명구\09_VectorStore\01_05_250122과제\로봇 공학에서의 인공지능 적용.pdf")

def extract_text_with_loader(loader_class, file_path):
    try:
        loader = loader_class(file_path)
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"{loader_class.__name__} 에러: {e}")
        return ""

def save_extracted_text(file_name, text):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    # 각 로더별 텍스트 추출
    loaders = {
        "PyPDFLoader": PyPDFLoader,
        "PyMuPDFLoader": PyMuPDFLoader,
        "PyPDFium2Loader": PyPDFium2Loader,
        "PDFMinerLoader": PDFMinerLoader,
        "PDFMinerPDFasHTMLLoader": PDFMinerPDFasHTMLLoader,
    }
    
    os.makedirs("extracted_texts", exist_ok=True)
    for loader_name, loader_class in loaders.items():
        print(f"{loader_name}로 텍스트 추출 중...")
        extracted_text = extract_text_with_loader(loader_class, FILE_PATH)
        save_extracted_text(f"extracted_texts/{loader_name}_text.txt", extracted_text)

    print("PDF 텍스트 추출 완료")
