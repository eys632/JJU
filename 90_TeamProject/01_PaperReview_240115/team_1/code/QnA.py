import os
from dotenv import load_dotenv
from loader import SecureFileLoader
from langchain_openai import ChatOpenAI  # langchain-openai 패키지에서 ChatOpenAI 임포트
from langchain.schema import SystemMessage, HumanMessage

def run_qna():
    """
    1) .env 로드
    2) data/QnA.yaml 및 data/research_paper.txt 로딩
    3) GPT 모델로 질문→답변 생성
    4) QnA.markdown 파일로 저장
    """
    # 1) .env 로드
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY가 설정되어 있지 않습니다.")
    
    # 2) QnA.yaml 로딩
    loader = SecureFileLoader(base_dir="data")
    try:
        qna_data = loader.load_yaml("QnA.yaml")
    except Exception as e:
        print(f"QnA.yaml 파일 로드 중 오류 발생: {e}")
        return

    # 연구 논문 로딩
    try:
        research_paper = loader.load_text("research_paper.txt")
    except Exception as e:
        print(f"research_paper.txt 파일 로드 중 오류 발생: {e}")
        research_paper = ""

    # 3) GPT 모델 초기화 (ChatGPT 계열)
    chat_model = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.0
    )

    # 시스템 메시지 구성 (논문 내용 포함)
    system_prompt = "You are a helpful assistant. Below is the content of a research paper to help you answer the following questions:\n\n"
    system_prompt += research_paper
    system_message = SystemMessage(content=system_prompt)
    
    # 4) 질문 목록 가져오기
    questions = qna_data.get("questions", [])
    if not questions:
        print("QnA.yaml에 'questions' 목록이 비어 있습니다.")
        return
    
    # 답변 저장용 리스트
    all_qa_results = []
    
    for item in questions:
        q_id = item.get("id", None)
        question = item.get("question", "")
        if not question:
            print(f"[WARNING] 질문이 비어있습니다 (id: {q_id})")
            continue

        # 질문 메시지 생성
        user_message = HumanMessage(content=question)
        messages = [system_message, user_message]
    
        # GPT 호출
        try:
            response = chat_model.invoke(messages)  # __call__ 대신 invoke 메서드 사용
            answer_text = response.content.strip()
        except Exception as e:
            print(f"[ERROR] GPT 호출 중 오류 (id={q_id}): {e}")
            answer_text = "Error generating response."
    
        # Q&A 결과를 저장용 리스트에 쌓기
        all_qa_results.append((q_id, question, answer_text))
    
    # 5) QnA.markdown 파일에 저장
    md_file_path = "data/QnA.markdown"  # 파일 경로가 'data/' 디렉토리에 있는지 확인
    try:
        with open(md_file_path, "w", encoding="utf-8") as f:
            # 파일에 마크다운 형식으로 기록
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