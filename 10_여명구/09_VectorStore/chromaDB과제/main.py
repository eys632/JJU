from pdf_loader import extract_text_with_loader, save_extracted_text
from chroma_db_setup import load_and_split_text, setup_chroma_db
from qa_generator import generate_questions, search_answers
from result_scorer import score_responses, save_results_to_json
from langchain_community.document_loaders import PyPDFLoader
import os

# 현재 디렉토리를 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "로봇 공학에서의 인공지능 적용.pdf")
# FILE_PATH = os.path.join(BASE_DIR, r"\로봇 공학에서의 인공지능 적용.pdf")

EXTRACTED_TEXT_DIR = os.path.join(BASE_DIR, "extracted_texts")
TEXT_FILE = os.path.join(EXTRACTED_TEXT_DIR, "pypdf_text.txt")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
RESULTS_FILE = os.path.join(BASE_DIR, "scored_results.json")

if __name__ == "__main__":
    # 1. PDF 텍스트 추출
    print("1. PDF 텍스트 추출")
    os.makedirs(EXTRACTED_TEXT_DIR, exist_ok=True)
    text = extract_text_with_loader(PyPDFLoader, FILE_PATH)
    save_extracted_text(TEXT_FILE, text)

    # 2. ChromaDB 설정
    print("2. ChromaDB 설정")
    split_docs = load_and_split_text(TEXT_FILE)
    chroma_db = setup_chroma_db(split_docs, DB_PATH, "documents")

    # 3. 질문 생성 및 검색
    print("3. 질문 생성 및 검색")
    questions = generate_questions()
    qa_results = search_answers(chroma_db, questions)

    # 4. 점수화 및 결과 저장
    print("4. 점수화 및 결과 저장")
    scored_results = score_responses(qa_results)
    save_results_to_json(scored_results, RESULTS_FILE)

    print(f"전체 작업 완료. 결과 파일: {RESULTS_FILE}")
