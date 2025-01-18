from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기 (필요하다면 사용)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

class TextSplitter:
    def __init__(self):
        pass

    def character_text_splitter(self, text: str) -> list:
        """
        CharacterTextSplitter를 사용하여 텍스트를 분할합니다.
        :param text: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        splitter = CharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        return splitter.split_text(text)

    def recursive_character_text_splitter(self, text: str) -> list:
        """
        RecursiveCharacterTextSplitter를 사용하여 텍스트를 재귀적으로 분할합니다.
        :param text: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        return splitter.split_text(text)

    def token_text_splitter(self, text: str) -> list:
        """
        tiktoken 기반 토크나이저를 사용하여 텍스트를 분할합니다.
        :param text: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=300,
            chunk_overlap=0,
        )
        return splitter.split_text(text)

    def semantic_chunker(self, text: str) -> list:
        """
        OpenAI 임베딩을 활용한 SemanticChunker로 텍스트를 의미 단위로 분할합니다.
        :param text: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        splitter = SemanticChunker(OpenAIEmbeddings())
        return splitter.split_text(text)
