from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question"),
    ResponseSchema(name="source", description="source used to answer the user's question, should be a website.")
]


output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    
        template = """answer the users question as best as possible,
        {format_instructions}
        {question}""",
        input_variables = ['question'],
        partial_variables = {'format_instructions': format_instructions},
)

model = ChatOpenAI(temperature = 0, model = 'gpt-4o')

chain = prompt | model | output_parser

response = chain.invoke({'question': '조선시대 왕들의 순서대로 알려줘'})

print(response)