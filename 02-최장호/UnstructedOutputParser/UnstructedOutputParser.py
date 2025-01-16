from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

os.environ['OPENAI_API_KEY'] = '****'
os.environ['LANGCHAIN_API_KEY'] = '****' # 본인 api
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = '03-03'

Response_Schemas = [
ResponseSchema(name='answer', description='사용자의 질문에 대한 답변'),
ResponseSchema(
    name='source',
    description="사용자의 질문에 답하기 위해 사용된 '출처', '웹사이트주소' 이어여 한다."
),

]

output_parser = StructuredOutputParser.from_response_schemas(Response_Schemas)

format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template='answer the users question as best as possible. \n{format_instructions}\n{question}',
    input_variables=['question'],
    partial_variables={"format_instructions" : format_instructions},
)

model = ChatOpenAI(
    temperature=0,
    model='gpt-4o'
)

chain = prompt | model | output_parser

response = chain.invoke({'question': 'EPL 19-20 시즌 토트넘 vs 아스날 경기 결과 알려줘줘 '})
print(response)