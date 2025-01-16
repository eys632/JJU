### 1. `mail_example.eml`

- 예제 이메일 파일로, `.eml` 형식의 이메일 내용을 담고 있습니다.
- 이메일의 메타데이터(발신자, 수신자, 제목 등)와 본문이 포함되어 있습니다.

### 2. `extract_email.py`

- `.eml` 파일에서 이메일 데이터를 추출하는 모듈입니다.

**주요 기능**:
- 발신자, 수신자, 제목, 날짜, 본문 데이터를 추출.
- 멀티파트 이메일도 처리 가능.

**사용 예시**:
```python
from extract_email import extract_email_data

email_data = extract_email_data("mail_example.eml")
print(email_data)

---

### 3. **`summarize_email.py`**

```markdown
### 3. `summarize_email.py`

- 추출된 이메일 본문을 GPT-4를 이용해 요약하고, 구조화된 JSON 데이터를 생성합니다.

**주요 기능**:
- 이메일 내용을 한국어로 요약.
- Pydantic 모델로 발신자, 수신자, 제목, 요약, 날짜를 JSON 형식으로 구조화.

**사용 예시**:
```python
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

---

### 4. **`save_json.py`**

```markdown
### 4. `save_json.py`

- 구조화된 데이터를 JSON 파일로 저장하는 모듈입니다.

**주요 기능**:
- Python 딕셔너리를 JSON 파일로 저장.
- 저장 시 읽기 쉽도록 들여쓰기 적용.

**사용 예시**:
```python
from save_json import save_to_json

data = {
    "sender": "example@domain.com",
    "recipient": "user@domain.com",
    "subject": "Example Subject",
    "summary": "This is a summarized email.",
    "date": "Mon, 13 Jan 2025 19:58:54 -0800"
}

save_to_json(data, "output.json")

---

### 5. **`main.py`**

```markdown
### 5. `main.py`

- 전체 파이프라인을 실행하는 메인 파일입니다.

**주요 기능**:
1. `.eml` 파일에서 이메일 데이터를 추출.
2. OpenAI GPT-4를 사용하여 이메일 본문을 요약.
3. 결과를 JSON 형식으로 저장.

**실행 예시**:
```bash
python main.py

---

### 6. **`.env`**

```markdown
### 6. `.env`

- 환경 변수 파일로, OpenAI API 키를 저장합니다.

**예시**:

- `.env` 파일은 `.gitignore`에 포함해 보안 문제를 방지합니다.
