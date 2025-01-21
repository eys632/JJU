# utils/env_utils.py
from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "USER_AGENT": os.getenv("USER_AGENT")
    }