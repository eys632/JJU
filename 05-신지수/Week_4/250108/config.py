from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# API 키 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 파일 확장자와 MIME 타입 매핑
EXTENSION_MIME_MAPPING = {
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

# 청크 설정
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 0

# 모델 설정
MODEL_NAME = "gpt-4o"
