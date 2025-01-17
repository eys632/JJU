import os
from typing import List, Dict, Tuple
from urllib.parse import urlparse
import mimetypes
from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredPDFLoader, PDFPlumberLoader,
    UnstructuredWordDocumentLoader, Docx2txtLoader,
    UnstructuredFileLoader, BSHTMLLoader, WebBaseLoader
)
from langchain.text_splitter import (
    CharacterTextSplitter, RecursiveCharacterTextSplitter,
    LatexTextSplitter
)
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class LoaderSplitterEvaluator:
    def __init__(self):
        # API 키들을 환경 변수에서 가져옴
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.chat_llm = ChatOpenAI(
            api_key=self.openai_api_key,
            model_name="gpt-4o"
        )
        
        # 파일 확장자와 MIME 타입 매핑 추가
        self.extension_mime_mapping = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/msword',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.htm': 'text/html',
            '.tex': 'text/latex',
            '.md': 'text/markdown',
            '.csv': 'text/csv',
            '.json': 'application/json',
            '.xml': 'application/xml'
        }

    def detect_input_type(self, input_path: str) -> str:
        """URL인지 파일인지 구분"""
        parsed = urlparse(input_path)
        if parsed.scheme and parsed.netloc:
            return "url"
        return "file"
    
    def get_file_type(self, file_path: str) -> str:
        """파일 형식 감지 (새로운 방식)"""
        # 파일 확장자 추출
        _, ext = os.path.splitext(file_path.lower())
        
        # 매핑된 MIME 타입 반환
        mime_type = self.extension_mime_mapping.get(ext)
        
        if mime_type:
            return mime_type
        
        # 확장자가 매핑되지 않은 경우
        try:
            # Python의 내장 mimetypes 모듈 사용
            guess_type = mimetypes.guess_type(file_path)[0]
            if guess_type:
                return guess_type
        except:
            pass
        
        # 기본값 반환
        return 'application/octet-stream'
    
    def get_available_loaders(self, input_type: str, file_type: str = None) -> List:
        """입력 타입에 따른 가능한 로더 목록 반환"""
        if (input_type == "url"):
            return [
                ("WebBaseLoader", WebBaseLoader),
                ("BSHTMLLoader", BSHTMLLoader)
            ]
        
        # 파일 타입별 로더 매핑
        loader_mapping = {
            "application/pdf": [
                ("PyPDFLoader", PyPDFLoader),
                ("UnstructuredPDFLoader", UnstructuredPDFLoader),
                ("PDFPlumberLoader", PDFPlumberLoader)
            ],
            "application/msword": [
                ("UnstructuredWordDocumentLoader", UnstructuredWordDocumentLoader),
                ("Docx2txtLoader", Docx2txtLoader)
            ],
            # 기타 파일 타입은 UnstructuredFileLoader 사용
            "default": [("UnstructuredFileLoader", UnstructuredFileLoader)]
        }
        
        return loader_mapping.get(file_type, loader_mapping["default"])
    
    def get_available_splitters(self, file_type: str) -> List:
        """파일 타입에 따른 가능한 스플리터 목록 반환"""
        splitter_mapping = {
            "application/pdf": [
                ("RecursiveCharacterTextSplitter", RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=0
                )),
                ("CharacterTextSplitter", CharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=0
                ))
            ],
            "text/html": [
                ("RecursiveCharacterTextSplitter", RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=0
                )),
                ("CharacterTextSplitter", CharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=0
                ))
            ],
            "text/latex": [
                ("LatexTextSplitter", LatexTextSplitter()),
                ("CharacterTextSplitter", CharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=0
                ))
            ],
            "default": [
                ("RecursiveCharacterTextSplitter", RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=0
                ))
            ]
        }
        return splitter_mapping.get(file_type, splitter_mapping["default"])
    
    def evaluate_combination(self, docs: List[Document]) -> int:
        """ChatLLM을 사용하여 결과물 평가"""
        # 평가 기준: 문서 구조 보존, 컨텍스트 유지, 청크 크기 적절성
        sample_text = docs[0].page_content if docs else ""
        evaluation_prompt = f"""
        다음 텍스트의 품질을 100점 만점으로 평가해주세요. 평가 기준:
        1. 문서 구조 보존
        2. 컨텍스트 완성도
        3. 청크 크기의 적절성
        
        텍스트: {sample_text[:500]}...
        
        점수만 숫자로 응답해주세요.
        """
        
        response = self.chat_llm.predict(evaluation_prompt)
        try:
            score = int(response.strip())
            return min(100, max(0, score))
        except:
            return 50  # 기본 점수
    
    def evaluate_all_combinations(self, input_path: str) -> List[Dict]:
        """모든 로더-스플리터 조합 평가"""
        input_type = self.detect_input_type(input_path)
        file_type = self.get_file_type(input_path) if input_type == "file" else "text/html"
        
        results = []
        loaders = self.get_available_loaders(input_type, file_type)
        splitters = self.get_available_splitters(file_type)
        
        for loader_name, loader_class in loaders:
            for splitter_name, splitter in splitters:
                try:
                    # 로더 실행
                    loader = loader_class(input_path)
                    docs = loader.load()
                    
                    # 스플리터 실행
                    split_docs = splitter.split_documents(docs)
                    
                    # 평가
                    score = self.evaluate_combination(split_docs)
                    
                    results.append({
                        "input_type": file_type,
                        "loader": loader_name,
                        "splitter": splitter_name,
                        "score": score
                    })
                except Exception as e:
                    print(f"Error with {loader_name}-{splitter_name}: {str(e)}")
                    continue
        
        # 점수로 정렬
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def print_results(self, results: List[Dict]):
        """결과 출력"""
        for idx, result in enumerate(results, 1):
            print(f"\n**{idx}순위**")
            print(f"1. input 파일형식: {result['input_type']}")
            print(f"2. package: {result['loader']} - {result['splitter']}")
            print(f"3. 평가 점수: {result['score']}/100")

# 사용 예시
def main():
    try:
        # 평가기 초기화 (API 키 파라미터 제거)
        evaluator = LoaderSplitterEvaluator()
        
        # 테스트할 파일 경로
        test_file = "C:/Python_workspace/bit/sub/data_all/02 논문작성법.pdf"
        
        print(f"파일 '{test_file}' 분석 중...")
        # 모든 가능한 로더-스플리터 조합 평가
        results = evaluator.evaluate_all_combinations(test_file)
        
        if not results:
            print("사용 가능한 로더/스플리터 조합을 찾을 수 없습니다.")
            return
            
        # 결과 출력
        print("\n=== 평가 결과 ===")
        evaluator.print_results(results)
        
        # 최적의 조합 출력
        best_result = results[0]
        print("\n최적의 조합:")
        print(f"로더: {best_result['loader']}")
        print(f"스플리터: {best_result['splitter']}")
        print(f"점수: {best_result['score']}/100")
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    main()
