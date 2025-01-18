# services/qna_service.py

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class QnAService:
    def __init__(self, research_paper_content):
        """
        연구 논문 내용을 초기화하고 GPT 모델을 설정합니다.
        """
        self.chat_model = ChatOpenAI(
            model_name="gpt-4o",  # 모델 이름 확인 필요 ("gpt-4o"가 올바른지 확인)
            temperature=0.0
        )
        self.research_paper_content = research_paper_content

    def get_answer(self, question):
        """
        질문을 받아 논문 내용과 함께 GPT 모델을 통해 답변을 생성합니다.
        """
        # 논문 내용과 질문을 결합
        combined_query = (
            "아래는 연구 논문의 내용입니다. 이를 참고하여 질문에 답변해 주세요.\n\n"
            + self.research_paper_content
            + "\n\n"
            + "질문: " + question
        )
        messages = [
            HumanMessage(content=combined_query)
        ]
        response = self.chat_model.invoke(messages)
        return response.content.strip()
