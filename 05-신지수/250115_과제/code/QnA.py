# Q&A.py

import os
from dotenv import load_dotenv
from loader import SecureFileLoader
from langchain.chat_models import ChatOpenAI  # 또는 OpenAIEmbeddings와 무관하게 ChatOpenAI만 import
from langchain.schema import SystemMessage, HumanMessage

def run_qna():
    """
    1) .env 로드
    2) data/Q&A.yaml 로딩
    3) GPT 모델로 질문→답변 생성
    4) Q&A.markdown 파일로 저장
    """
    # 1) .env 로드
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    # 2) Q&A.yaml 로딩
    loader = SecureFileLoader(base_dir="data")
    try:
        qna_data = loader.load_yaml("QnA.yaml")
    except Exception as e:
        print(f"QnA.yaml 파일 로드 중 오류 발생: {e}")
        return

    # 3) GPT 모델 초기화 (ChatGPT 계열)
    chat_model = ChatOpenAI(
        model_name="gpt-4",  # gpt-3.5-turbo 등 원하는 모델
        temperature=0.0
    )

    # 질문 목록 가져오기
    questions = qna_data.get("questions", [])
    if not questions:
        print("QnA.yaml에 'questions'가 비어 있습니다.")
        return

    all_qa_results = []
    for item in questions:
        q_id = item.get("id", None)
        question = item.get("question", "")
        if not question:
            print(f"[WARNING] 질문이 비어있습니다 (id: {q_id})")
            continue

        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=question)
        ]

        try:
            response = chat_model(messages)
            answer_text = response.content.strip()
        except Exception as e:
            print(f"[ERROR] GPT 호출 중 오류 (id={q_id}): {e}")
            answer_text = "Error generating response."
        
        all_qa_results.append((q_id, question, answer_text))

    # 4) Q&A.markdown 파일에 저장
    md_file_path = "QnA.markdown"
    try:
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write("# QnA 결과\n\n")
            for q_id, question, answer in all_qa_results:
                f.write(f"## Q{q_id if q_id else ''}. {question}\n")
                f.write(f"- **Answer**: {answer}\n\n")
        print(f"답변이 '{md_file_path}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"[ERROR] 결과 저장 중 오류: {e}")

# 이 모듈을 직접 실행할 수도 있음
if __name__ == "__main__":
    run_qna()
