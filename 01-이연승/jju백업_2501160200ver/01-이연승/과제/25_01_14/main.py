from extract_email import extract_email_data
from summarize_email import summarize_email
from save_json import save_to_json
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 불러오기
load_dotenv()

if __name__ == "__main__":
    # 환경 변수에서 API 키 가져오기
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key not found. Please ensure OPENAI_API_KEY is set in your .env file.")

    # 파일 경로 설정
    eml_file = r"C:\Users\eys63\github\JJU\01-이연승\과제\25_01_14\mail_example.eml"
    output_file = r"C:\Users\eys63\github\JJU\01-이연승\과제\25_01_14\reply-structured.json"

    # 1. 이메일 데이터 추출
    email_data = extract_email_data(eml_file)

    # 2. 이메일 요약 처리
    structured_data = summarize_email(email_data, api_key)

    # 3. JSON 파일로 저장
    save_to_json(structured_data, output_file)

    print(f"Email data successfully processed and saved to {output_file}")
