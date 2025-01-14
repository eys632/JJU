# 필요한 라이브러리 설치 안내:
# 터미널에서 아래 명령어를 실행하세요.
# ! pip install langchain_community unstructured

from langchain_community.document_loaders import DirectoryLoader, TextLoader, PythonLoader

# DirectoryLoader 초기화 함수
def init_directory_loader(path, glob_pattern, show_progress=False, use_multithreading=False, loader_cls=None):
    """
    DirectoryLoader를 초기화하는 함수.
    - path: 탐색할 디렉토리 경로
    - glob_pattern: 검색할 파일의 패턴 (예: **/*.md)
    - show_progress: 진행 상태를 출력할지 여부
    - use_multithreading: 멀티스레딩 사용 여부
    - loader_cls: 특정 로더 클래스 (TextLoader, PythonLoader 등) 사용
    """
    return DirectoryLoader(
        path,
        glob=glob_pattern,
        show_progress=show_progress,
        use_multithreading=use_multithreading,
        loader_cls=loader_cls
    )

# Markdown 파일 로드 함수
def load_markdown_files(path="./", glob_pattern="**/*.md", show_progress=False, use_multithreading=False):
    """
    DirectoryLoader를 사용하여 Markdown 파일을 로드하는 함수.
    - path: 탐색할 디렉토리 경로
    - glob_pattern: 검색할 파일의 패턴
    - show_progress: 진행 상태를 출력할지 여부
    - use_multithreading: 멀티스레딩 사용 여부
    """
    loader = init_directory_loader(path, glob_pattern, show_progress, use_multithreading, loader_cls=TextLoader)
    try:
        docs = loader.load()
    except Exception as e:
        print(f"Error loading documents: {e}")
        docs = []
    return docs

# TextLoader를 사용한 Markdown 파일 로드 함수
def load_text_files(path="./", glob_pattern="**/*.md", encoding="utf-8"):
    """
    TextLoader를 사용하여 Markdown 파일을 로드하는 함수.
    - path: 탐색할 디렉토리 경로
    - glob_pattern: 검색할 파일의 패턴
    - encoding: 파일의 인코딩 형식 (기본값: utf-8)
    """
    try:
        loader = DirectoryLoader(
            path,
            glob=glob_pattern,
            loader_cls=lambda file_path: TextLoader(file_path, encoding=encoding)
        )
        docs = loader.load()
    except Exception as e:
        print(f"Error loading documents: {e}")
        docs = []
    return docs

# Python 파일 로드 함수
def load_python_files(path="./", glob_pattern="**/*.py"):
    """
    PythonLoader를 사용하여 Python 파일을 로드하는 함수.
    - path: 탐색할 디렉토리 경로
    - glob_pattern: 검색할 파일의 패턴
    """
    loader = init_directory_loader(path, glob_pattern, loader_cls=PythonLoader)
    docs = loader.load()
    return docs

# 메인 함수
def main():
    # Markdown 파일 로드 예제
    print("Markdown 파일 로드 중...")
    md_docs = load_markdown_files(show_progress=True)
    print(f"총 {len(md_docs)}개의 Markdown 문서를 로드했습니다.")
    
    # 첫 번째 문서 내용 일부 출력
    if md_docs:
        print("첫 번째 문서 내용 (미리보기):")
        print(md_docs[0].page_content[:200])
    
    # TextLoader를 사용한 Markdown 파일 로드 예제
    print("\nTextLoader를 사용하여 Markdown 파일 로드 중...")
    text_docs = load_text_files(encoding="utf-8")
    print(f"총 {len(text_docs)}개의 Text 문서를 로드했습니다.")
    
    if text_docs:
        print("첫 번째 문서 내용 (미리보기):")
        print(text_docs[0].page_content[:200])
    
    # Python 파일 로드 예제
    print("\nPython 파일 로드 중...")
    py_docs = load_python_files()
    print(f"총 {len(py_docs)}개의 Python 문서를 로드했습니다.")

    # 로드된 Python 문서들 중 일부를 출력하여 내용 확인
    for i, doc in enumerate(py_docs[:3]):
        print(f"Python 문서 {i + 1} (미리보기):")
        print(doc.page_content[:200])
        print("-" * 50)

    

# Python 스크립트 실행
if __name__ == "__main__":
    main()
