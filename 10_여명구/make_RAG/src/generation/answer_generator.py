# src/generation/answer_generator.py
import openai
import os

class AnswerGenerator:
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY", "")
        self.model = model
        openai.api_key = self.api_key

    def generate_answer(self, query: str, retrieved_docs: list, max_tokens: int = 500) -> str:
        context = ""
        for (meta, score) in retrieved_docs:
            content_snippet = meta.get("content", "")
            source = meta.get("source", "unknown")
            page = meta.get("page", "N/A")
            context += f"- Source: {source} (Page {page}), Score: {score}\n"
            context += f"  {content_snippet}\n\n"

        prompt = (
            f"질문: {query}\n\n"
            f"아래 문서 내용을 참고하여 간결하고 정확한 답변을 작성해줘:\n"
            f"{context}\n"
            f"답변:"
        )

        # 최신 1.0+ 문법 (예시): openai.chat_completions.create(...)
        response = openai.chat_completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 전문적인 지식을 바탕으로 답변하는 AI 어시스턴트입니다."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
