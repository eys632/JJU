import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 세션 상태에서 메시지 리스트 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 필요한 세션 상태 키가 없으면 초기화
# (단, '입력용 key'는 초기화를 굳이 미리 안 해줘도 되지만 안전 차원에서 선언)
if "error_message_input" not in st.session_state:
    st.session_state["error_message_input"] = ""
if "error_code_input" not in st.session_state:
    st.session_state["error_code_input"] = ""

def run_llm(error_msg: str, error_code: str):
    """
    LLM 호출 및 결과 처리 함수.
    정상적으로 완료된 경우 입력 필드를 비웁니다.
    """
    user_input = f"""
    에러 메시지: {error_msg}
    코드: {error_code}

    지침:
    - 에러가 다시 발생하지 않도록 작성.
    - 응답은 코드와 설명(Description)으로 나누어 제공.
    - 먼저 수정된 코드를 제시.
    - 이후 코드 뒤에 수정 이유와 증상을 설명.
    - Description은 반드시 한글로 작성.
    """

    # 사용자 입력 메시지를 세션 상태에 저장
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # ChatOpenAI 모델 초기화
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)

    # LLM 응답 생성 및 스트리밍 출력
    with st.spinner("답변 작성 중..."):
        try:
            human_message = HumanMessage(content=user_input)

            # 이전 답변 출력
            if st.session_state["messages"]:
                for idx, msg in enumerate(st.session_state["messages"]):
                    if msg["role"] == "assistant":
                        st.markdown("---")  # 답변 구분선
                        st.write(msg["content"])  # 최종 응답만 표시

            # 새로운 스트리밍 응답 출력
            assistant_response = ""
            st.markdown("---")  # 새로운 답변 구분선
            response_container = st.empty()

            for chunk in llm.stream([human_message]):
                assistant_response += chunk.content
                response_container.markdown(assistant_response)

            # 새로운 응답을 세션 상태에 저장
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response})
            st.markdown("---")  # 새로운 답변 끝에 구분선

            # 모든 처리가 끝난 후, 입력 필드 비우기
            st.session_state["error_message_input"] = ""
            st.session_state["error_code_input"] = ""

        except Exception as e:
            st.error(f"오류 발생: {e}")

# 사이드바에서 입력 필드와 실행 버튼 생성
with st.sidebar:
    st.title("오류 수정 도우미")
    st.caption("OpenAI GPT-4o를 사용하여 오류를 분석하고 수정합니다.")

    # '입력용 key'를 별도로 사용
    st.text_area("에러 메시지",
                 placeholder="여기에 에러 메시지를 입력하세요...",
                 key="error_message_input")
    st.text_area("코드",
                 placeholder="여기에 코드를 입력하세요...",
                 key="error_code_input")

    # 'Run' 버튼 클릭 시 LLM 요청 처리
    if st.button("Run"):
        # OpenAI API Key 미설정 시 경고
        if not OPENAI_API_KEY:
            st.warning("OpenAI API Key를 설정해주세요.")
        # 에러 메시지나 코드가 공백이면 경고
        elif not st.session_state["error_message_input"].strip() and not st.session_state["error_code_input"].strip():
            st.warning("에러 메시지나 코드를 입력해주세요.")
        else:
            run_llm(
                st.session_state["error_message_input"],
                st.session_state["error_code_input"],
            )
