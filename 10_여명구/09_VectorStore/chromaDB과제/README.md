# YETI Framework Analysis

## 프로젝트 설명
YETI 프레임워크를 분석하고, 관련 PDF 파일에서 텍스트를 추출하여 ChromaDB를 구축한 뒤, 질문-답변 기반 점수를 계산하는 프로젝트입니다. 이 프로젝트는 PDF 파일 처리, 질의응답 생성, 유사도 기반 검색, 점수화 및 결과 저장의 전체 작업 흐름을 포함합니다.

---

## 주요 기능
1. **PDF 텍스트 추출**:
   - 다양한 PDF 로더(PyPDFLoader, PyMuPDFLoader 등)를 사용해 PDF에서 텍스트를 추출합니다.

2. **ChromaDB 구축**:
   - 추출된 텍스트를 분할하고 OpenAI 임베딩을 활용하여 ChromaDB를 생성합니다.

3. **질의응답 생성 및 검색**:
   - 미리 정의된 질문 리스트를 기반으로 ChromaDB에서 유사한 텍스트를 검색합니다.

4. **점수 계산**:
   - 질문과 답변의 유사도, 답변 길이, 키워드 포함 여부를 기반으로 점수를 계산합니다.

5. **결과 저장**:
   - 점수화된 결과를 JSON 파일로 저장합니다.

---

## 파일 구조
```
chromaDB과제제/
├── main.py                       # 전체 실행 스크립트
├── pdf_loader.py                 # PDF 텍스트 추출 모듈
├── chroma_db_setup.py            # ChromaDB 설정 및 생성
├── qa_generator.py               # 질문 생성 및 검색
├── result_scorer.py              # 점수 계산 및 저장
├── extracted_texts/              # PDF에서 추출된 텍스트 저장 디렉토리
├── .env                          # OpenAI API 키 설정 파일
├── .gitignore
│   ├── PyPDFLoader_text.txt
│   ├── PyMuPDFLoader_text.txt
│   ...
├── chroma_db/                    # ChromaDB 파일 저장 디렉토리
├── scored_results.json           # 점수화된 결과 파일
└── 로봇 공학에서의 인공지능 적용.pdf  # PDF 파일
```

---

## 실행 방법

### 1. 환경 설정
#### 필수 라이브러리 설치
다음 명령어를 통해 필요한 Python 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

#### `.env` 파일 설정
`.env` 파일을 생성하고 OpenAI API 키를 입력합니다:
```
OPENAI_API_KEY=your_openai_api_key
```

### 2. PDF 텍스트 추출
다양한 PDF 로더를 사용하여 PDF 파일에서 텍스트를 추출합니다:
```bash
python pdf_loader.py
```

### 3. ChromaDB 생성
추출된 텍스트를 기반으로 ChromaDB를 생성합니다:
```bash
python chroma_db_setup.py
```

### 4. 질의응답 및 점수 계산
질문 리스트를 기반으로 ChromaDB에서 검색을 수행하고, 점수를 계산한 뒤 결과를 저장합니다:
```bash
python main.py
```

---

## 주요 설정 및 변수
- `TEXT_FILE`: 추출된 텍스트 파일 경로.
- `DB_PATH`: ChromaDB 저장 디렉토리 경로.
- `RESULTS_FILE`: 점수화된 결과 저장 파일 경로.
- `chunk_size`: 텍스트 분할 크기 (기본값: 600).

---

## 결과물
### 출력 파일
1. **텍스트 파일**:
   - `extracted_texts/` 디렉토리에 저장된 각 로더별 텍스트 추출 결과.

2. **ChromaDB**:
   - `chroma_db/` 디렉토리에 저장된 벡터 데이터베이스.

3. **점수화 결과**:
   - `scored_results.json` 파일에 저장된 질문-답변 점수 결과.

### 예시 결과
```json
[
    {
        "질문": "YETI 프레임워크는 기존 HoloAssist와 비교했을 때 어떤 주요 개선점을 제공하는가?",
        "답변": "YETI provides enhanced accuracy by leveraging both Global and Local contexts, enabling better understanding of user intentions.",
        "점수": 6.45
    },
    ...
]
```

---