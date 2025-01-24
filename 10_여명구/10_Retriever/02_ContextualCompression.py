from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_teddynote.document_compressors import LLMChainExtractor, LLMChainFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter, DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain_openai import ChatOpenAI
# pip install faiss-cpu

# 환경 변수 로드
load_dotenv()

# 문서 로더 초기화
def initialize_loader(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
    return loader.load_and_split(text_splitter)

# 리트리버 초기화
def initialize_retriever(texts):
    embeddings = OpenAIEmbeddings()
    retriever = FAISS.from_documents(texts, embeddings).as_retriever()
    return retriever

# 문서 압축 리트리버 생성 함수
def create_compression_retriever(retriever, compressor):
    return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

# 문서 출력 함수
def pretty_print_docs(docs, title):
    print(f"\n=== {title} ===")
    for i, doc in enumerate(docs, 1):
        print(f"문서 {i}:\n{doc.page_content}\n{'-' * 100}")

# 메인 실행 함수
def main():
    # 데이터 로드 및 리트리버 생성
    file_path = r"10_여명구\data\appendix-keywords.txt"
    texts = initialize_loader(file_path)
    retriever = initialize_retriever(texts)

    # 기본 검색
    docs = retriever.invoke("Semantic Search 에 대해서 알려줘.")
    pretty_print_docs(docs, "기본 검색 결과")

    # LLMChainExtractor 압축기 사용
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    extractor = LLMChainExtractor.from_llm(llm)
    compression_retriever = create_compression_retriever(retriever, extractor)
    compressed_docs = compression_retriever.invoke("Semantic Search 에 대해서 알려줘.")
    pretty_print_docs(compressed_docs, "LLMChainExtractor 압축 결과")

    # LLMChainFilter 압축기 사용
    filter_compressor = LLMChainFilter.from_llm(llm)
    compression_retriever = create_compression_retriever(retriever, filter_compressor)
    compressed_docs = compression_retriever.invoke("Semantic Search 에 대해서 알려줘.")
    pretty_print_docs(compressed_docs, "LLMChainFilter 압축 결과")

    # EmbeddingsFilter 압축기 사용
    embeddings_filter = EmbeddingsFilter(embeddings=OpenAIEmbeddings(), similarity_threshold=0.86)
    compression_retriever = create_compression_retriever(retriever, embeddings_filter)
    compressed_docs = compression_retriever.invoke("Semantic Search 에 대해서 알려줘.")
    pretty_print_docs(compressed_docs, "EmbeddingsFilter 압축 결과")

    # DocumentCompressorPipeline 압축기 사용
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
    redundant_filter = EmbeddingsRedundantFilter(embeddings=OpenAIEmbeddings())
    pipeline_compressor = DocumentCompressorPipeline(
        transformers=[splitter, redundant_filter, embeddings_filter, extractor]
    )
    compression_retriever = create_compression_retriever(retriever, pipeline_compressor)
    compressed_docs = compression_retriever.invoke("Semantic Search 에 대해서 알려줘.")
    pretty_print_docs(compressed_docs, "DocumentCompressorPipeline 압축 결과")

if __name__ == "__main__":
    main()
