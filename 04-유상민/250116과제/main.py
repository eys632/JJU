from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


output_parser = CommaSeparatedListOutputParser()

format_instruction = output_parser.get_format_instructions()

prompt = PromptTemplate(

    template = 'List five {subject}.\n{format_instructions}',
    input_variables = ['subject'],
    partial_variables = {'format_instructions': format_instruction},


)

model = ChatOpenAI(temperature = 0)

chain = prompt | model | output_parser

response = chain.invoke({'subject':'한국인이 제일 좋아하는 아이스크림 종류 5가지'})

print(response)

