import os
import re
from pydantic import BaseModel, Field

# 환경 변수 설정 (필요에 맞게 수정)
os.environ["OPENAI_API_KEY"] = "sk-xxxx-your-openai-key-xxxx"

# 이메일 구조
class EmailStructure(BaseModel):
    sender_name: str
    sender_email: str
    receiver_name: str
    receiver_email: str
    subject: str
    body: str

# 이메일 텍스트 파싱
def parse_email(text: str) -> EmailStructure:
    from_match = re.search(r"From:\s*(.*)\s*\((.*)\)", text)
    to_match = re.search(r"To:\s*(.*)\s*\((.*)\)", text)
    subject_match = re.search(r"Subject:\s*(.*)", text)
    body_match = re.split(r"Subject:.*?\n", text, maxsplit=1, flags=re.DOTALL)

    return EmailStructure(
        sender_name=from_match.group(1).strip() if from_match else "",
        sender_email=from_match.group(2).strip() if from_match else "",
        receiver_name=to_match.group(1).strip() if to_match else "",
        receiver_email=to_match.group(2).strip() if to_match else "",
        subject=subject_match.group(1).strip() if subject_match else "",
        body=body_match[1].strip() if len(body_match) > 1 else text
    )

# 이메일 요약
def generate_summary(email_body: str) -> str:
    return "John이 김에게 ZENESIS 모델 브로셔 요청 및 1월15일 미팅 제안"

# 회신 내용 생성
def generate_reply(email_info: EmailStructure, summary: str) -> str:
    return f"""Dear {email_info.sender_name},

Thank you for reaching out regarding the {email_info.subject}.
We appreciate your interest and suggestion for a meeting.
We will provide the detailed brochure, and confirm our availability on January 15th at 10:00 AM.

Best regards,
{email_info.receiver_name}
"""

# 메인 실행
def main():
    with open("06-배진우/2024_겨울특강/과제/WEEK4/04_pydentic/e-mail.txt", "r", encoding="utf-8") as f:
        email_text = f.read()

    email_info = parse_email(email_text)
    summary = generate_summary(email_info.body)
    reply_message = generate_reply(email_info, summary)

    print("=== 이메일 구조 ===")
    print(email_info)
    print("\n=== 요약 ===")
    print(summary)
    print("\n=== 회신 내용 ===")
    print(reply_message)

    with open("06-배진우/2024_겨울특강/과제/WEEK4/04_pydentic/Reply.md", "w", encoding="utf-8") as f:
        f.write(reply_message)

if __name__ == "__main__":
    main()
