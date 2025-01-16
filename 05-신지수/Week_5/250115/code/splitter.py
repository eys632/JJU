from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import os

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기 (필요하다면 사용)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

class text_splitter:
    def __init__(self):
        pass

    def CharacterTextSplitter(self, file: str):
        """
        CharacterTextSplitter를 사용하여 텍스트를 분할합니다.
        :param file: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        text_splitter = CharacterTextSplitter(
            # 텍스트를 분할할 때 사용할 구분자를 지정합니다. 기본값은 "\n\n"입니다.
            # separator=" ",
            # 분할된 텍스트 청크의 최대 크기를 지정합니다.
            chunk_size=250,
            # 분할된 텍스트 청크 간의 중복되는 문자 수를 지정합니다.
            chunk_overlap=50,
            # 텍스트의 길이를 계산하는 함수를 지정합니다.
            length_function=len,
            # 구분자가 정규식인지 여부를 지정합니다.
            is_separator_regex=False,
        )
        # 텍스트를 청크 단위로 분할합니다.
        splitted_texts = text_splitter.split_text(file)
        return splitted_texts

    def RecursiveCharacterTextSplitter(self, file: str):
        """
        RecursiveCharacterTextSplitter를 사용하여 텍스트를 재귀적으로 분할합니다.
        :param file: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        text_splitter = RecursiveCharacterTextSplitter(
            # 청크 크기
            chunk_size=250,
            # 청크 간의 중복되는 문자 수
            chunk_overlap=50,
            # 문자열 길이 계산 함수
            length_function=len,
            # 구분자로 정규식을 사용할지 여부
            is_separator_regex=False,
        )
        # 텍스트를 청크 단위로 분할합니다.
        splitted_texts = text_splitter.split_text(file)
        return splitted_texts

    def TokenTextSplitter(self, file: str):
        """
        tiktoken 기반 토크나이저를 사용하여 텍스트를 분할합니다.
        :param file: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            # 청크 크기를 300으로 설정합니다.
            chunk_size=300,
            # 청크 간 중복되는 부분이 없도록 설정합니다.
            chunk_overlap=0,
        )
        # 텍스트를 청크 단위로 분할합니다.
        splitted_texts = text_splitter.split_text(file)
        return splitted_texts

    def SemanticChunker(self, file: str):
        """
        OpenAI 임베딩을 활용한 SemanticChunker로 텍스트를 의미 단위로 분할합니다.
        :param file: 분할할 텍스트(문자열)
        :return: 분할된 텍스트 청크 리스트
        """
        # 필요에 따라 다시 .env 로드 (이미 상단에서 로드했다면 생략 가능)
        load_dotenv()

        # OpenAI 임베딩을 사용하여 의미론적 청크 분할기를 초기화합니다.
        # (API 키가 이미 환경 변수에 세팅되어 있다면 그대로 사용됩니다)
        text_splitter = SemanticChunker(OpenAIEmbeddings())
        splitted_texts = text_splitter.split_text(file)
        return splitted_texts
