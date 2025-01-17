from langchain.chat_models import ChatOpenAI

def create_llm(api_key: str, model_name="gpt-4", temperature=0):
    """LLM 객체 생성"""
    return ChatOpenAI(
        temperature=temperature,
        model=model_name,
        openai_api_key=api_key
    )

def get_response(llm, prompt, question):
    """LLM에 질문을 전달하고 응답받기"""
    chain = prompt | llm
    result = chain.invoke({"question": question})
    return result.content
