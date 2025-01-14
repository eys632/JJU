이메일 요약 및 구조화 프로젝트
이 프로젝트는 .eml 형식의 이메일 파일을 읽어 발신자, 수신자, 제목, 본문 요약, 날짜 등의 정보를 추출하고, 이를 JSON 형식으로 저장하는 간단한 파이프라인을 제공합니다.

이 코드는 OpenAI의 GPT-4를 사용하여 이메일 본문을 요약하며, Pydantic 모델을 활용해 구조화된 JSON 데이터를 생성합니다.

프로젝트 파일 구조
bash
코드 복사
C:\Users\eys63\github\JJU\01-이연승\과제\25_01_14\
├── mail_example.eml      # 예제 이메일 파일
├── extract_email.py       # 이메일 데이터 추출
├── summarize_email.py     # 이메일 요약 처리
├── save_json.py           # JSON 저장
├── main.py                # 메인 실행 파일
├── .env                   # 환경 변수 파일 (업로드 제외)
├── reply-structured.json  # 실행 결과 저장 파일 (자동 생성)
주요 파일 설명
1. mail_example.eml
예제 이메일 파일로, .eml 형식의 이메일 내용을 담고 있습니다. 이메일의 메타데이터(발신자, 수신자, 제목 등)와 본문이 포함되어 있습니다.

2. extract_email.py
.eml 파일에서 이메일 데이터를 추출하는 모듈입니다.

주요 기능:

발신자, 수신자, 제목, 날짜, 본문 데이터를 추출.
멀티파트 이메일도 처리 가능.
사용 예시:

python
코드 복사
from extract_email import extract_email_data

email_data = extract_email_data("mail_example.eml")
print(email_data)
3. summarize_email.py
추출된 이메일 본문을 GPT-4를 이용해 요약하고, 구조화된 JSON 데이터를 생성하는 모듈입니다.

주요 기능:

이메일 내용을 한국어로 요약.
Pydantic 모델로 발신자, 수신자, 제목, 요약, 날짜를 JSON 형식으로 구조화.
사용 예시:

python
코드 복사
from summarize_email import summarize_email

api_key = "your_openai_api_key"
email_data = {
    "sender": "example@domain.com",
    "recipient": "user@domain.com",
    "subject": "Example Subject",
    "date": "Mon, 13 Jan 2025 19:58:54 -0800",
    "body": "This is an example email body."
}

summary = summarize_email(email_data, api_key)
print(summary)
4. save_json.py
구조화된 데이터를 JSON 파일로 저장하는 모듈입니다.

주요 기능:

Python 딕셔너리를 JSON 파일로 저장.
저장 시 읽기 쉽도록 들여쓰기 적용.
사용 예시:

python
코드 복사
from save_json import save_to_json

data = {
    "sender": "example@domain.com",
    "recipient": "user@domain.com",
    "subject": "Example Subject",
    "summary": "This is a summarized email.",
    "date": "Mon, 13 Jan 2025 19:58:54 -0800"
}

save_to_json(data, "output.json")
5. main.py
전체 파이프라인을 실행하는 메인 파일입니다.

주요 기능:

.eml 파일에서 이메일 데이터를 추출.
OpenAI GPT-4를 사용하여 이메일 본문을 요약.
결과를 JSON 형식으로 저장.
실행 예시:

bash
코드 복사
python main.py
실행 후 reply-structured.json 파일이 생성되며, 이메일의 구조화된 요약 데이터가 저장됩니다.

6. .env
환경 변수 파일로, OpenAI API 키를 저장합니다.

예시:

makefile
코드 복사
OPENAI_API_KEY=your_actual_api_key
.env 파일은 .gitignore에 포함하여 버전에 포함되지 않도록 관리합니다.

실행 방법
필요한 라이브러리 설치:

bash
코드 복사
pip install python-dotenv openai langchain-openai langchain-core pydantic
.env 파일 설정: 프로젝트 루트에 .env 파일을 생성하고 OpenAI API 키를 추가:

makefile
코드 복사
OPENAI_API_KEY=your_actual_api_key
main.py 실행:

bash
코드 복사
python main.py
결과 확인: reply-structured.json 파일에서 이메일 요약 데이터를 확인할 수 있습니다.

실행 결과
reply-structured.json 예시:

json
코드 복사
{
    "sender": "Notion Team <notify@mail.notion.so>",
    "recipient": "eys632@gmail.com",
    "subject": "새 기기의 최근 로그인 감토",
    "summary": "Notion 계정으로 새 기기에서 로그인된 활동이 감지되었습니다. 세부 정보를 확인하거나 문제가 있으면 설정에서 계정을 보호하세요.",
    "date": "Tue, 14 Jan 2025 03:58:54 +0000"
}
주의 사항
.env 파일은 프로젝트 루트에 있어야 하며, API 키가 올바르게 설정되어야 합니다.
.env 파일은 .gitignore에 포함해 보안 문제를 방지합니다.
이 프로젝트를 통해 .eml 파일에서 이메일 데이터를 추출하고 요약하여 JSON 형식으로 저장하는 과정을 간단히 처리할 수 있습니다. 필요하면 자유롭게 수정하고 활용하세요! 😊
