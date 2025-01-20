# src/loaders/__init__.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

"""
이곳에서 .env를 로드해두면, loaders 모듈 내부 어디서든
OPENAI_API_KEY 변수를 임포트해 사용할 수 있습니다.
"""
