import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

def main():
    # 1) 분할된 텍스트가 저장된 디렉토리
    splitted_folder = "C:\\Users\\eys63\\GitHub\\JJU\\01-이연승\\과제\\25_01_22과제_ChromaDB\\split_output"
    # 2) Chroma DB를 저장할 경로
    db_path = "C:\\Users\\eys63\\GitHub\\JJU\\01-이연승\\과제\\25_01_22과제_ChromaDB\\chroma_db"

    # (1) 분할된 텍스트 파일 로드 → LangChain의 Document 리스트 구성
    docs = []
    for file_name in os.listdir(splitted_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(splitted_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            # LangChain 형식의 Document 객체에 담아둠
            docs.append(Document(page_content=text, metadata={"source": file_name}))

    # (2) 임베딩 모델 설정 (HuggingFace 기반)
    # sentence-transformers/all-MiniLM-L6-v2 모델 사용
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # (3) Chroma VectorStore 생성
    # from_documents() → 문서 리스트를 임베딩하여, 로컬에 영구저장(persist_directory)함
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=db_path
    )

    # (4) DB 영구 저장
    vectordb.persist()

    # (5) 검색 테스트
    query = "검색할 내용을 입력하세요"
    results = vectordb.similarity_search(query, k=5)

    # 결과 출력
    print("\n검색 결과:")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"[Source: {doc.metadata['source']}]")
        print(doc.page_content[:300], "...")
        # 필요하다면 doc.page_content 전체 또는 상위 n자 출력

if __name__ == "__main__":
    main()
