from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(temperature = 0, model_name="gpt-4o")

class Topic(BaseModel):
    description: str = Field(description="주제에 대한 간결한 설명")
    hastags: str = Field(description="해시태그 형식의 키워드(2개 이상)")

parser = JsonOutputParser(pydantic_object=Topic)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI어시스턴트입니다. 질문에 간결하게 답변하세요."),
        ("user", "Format: {format_instruction}\n\nQuestion: {question}"),
    ]
)

prompt = prompt.partial(format_instruction  = parser.get_format_instructions)

chain = prompt | model | parser

question = '유튜브의 폐헤에 대해 알려줘'
answer = chain.invoke({"question": question})
print(answer)