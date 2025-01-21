# services/search_service.py

import logging
from functools import lru_cache  # lru_cache 임포트
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from splitter import TextSplitter

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, data: str):
        self.data = data
        self.splitter = TextSplitter()
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self.initialize_vector_store()

    @lru_cache(maxsize=1)  # 캐싱 데코레이터 적용
    def initialize_vector_store(self) -> FAISS:
        """
        텍스트 청크의 임베딩을 생성하고 FAISS 벡터 스토어를 초기화합니다.
        이 메서드는 캐싱되어 동일한 데이터에 대해 반복 호출 시 캐시된 결과를 반환합니다.
        
        :return: FAISS 벡터 스토어 객체
        """
        try:
            # 텍스트 분할
            text_chunks = self.splitter.semantic_chunker(self.data)
            logger.info(f"텍스트를 {len(text_chunks)}개의 청크로 분할했습니다.")
            
            # FAISS 벡터 스토어 초기화
            vector_store = FAISS.from_texts(text_chunks, self.embeddings)
            logger.info("FAISS 벡터 스토어를 초기화했습니다.")
            
            return vector_store
        except Exception as e:
            logger.error(f"벡터 스토어 초기화 중 오류 발생: {e}")
            return None

    def search(self, query: str, top_k: int = 5) -> list:
        """
        사용자 쿼리에 대한 상위 k개의 관련 문서 검색

        :param query: 검색할 질문 또는 쿼리
        :param top_k: 반환할 문서의 수
        :return: 관련 문서 리스트
        """
        if not self.vector_store:
            logger.error("벡터 스토어가 초기화되지 않았습니다.")
            return []
        
        try:
            # 쿼리 임베딩 생성 및 유사도 검색
            results = self.vector_store.similarity_search(query, k=top_k)
            logger.info(f"상위 {top_k}개의 관련 문서를 검색했습니다.")
            return [result.page_content for result in results]
        except Exception as e:
            logger.error(f"검색 중 오류 발생: {e}")
            return []
