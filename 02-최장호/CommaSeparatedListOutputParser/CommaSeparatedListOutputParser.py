from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

os.environ['OPENAI_API_KEY'] = '****'
os.environ['LANGCHAIN_API_KEY'] = '****' 
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = '03-02-03'

output_parser = CommaSeparatedListOutputParser()

format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
        template="List five {subject}.\n{format_instructions}",
        input_variables=['subject'], #입력 변수수
        partial_variables={"format_instructions": format_instructions}, #부분변수
)

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o'
)

chain = prompt|llm|output_parser

response = chain.invoke('토트넘 선수 알려줘')

print(response)
