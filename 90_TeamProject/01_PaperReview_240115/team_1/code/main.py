# main.py

import os
from dotenv import load_dotenv
from QnA import run_qna 

def main():
    load_dotenv()
    print("=== Q&A 프로세스 시작 ===")
    run_qna()
    print("=== Q&A 프로세스 종료 ===")

if __name__ == "__main__":
    main()
