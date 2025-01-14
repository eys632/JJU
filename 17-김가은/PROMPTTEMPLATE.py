import os

os.environ["OPENAI_API_KEY"] = ""
os.environ['LANGCHAIN_API_KEY'] = ""
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = ''
os.environ['LANGCHAIN_PROJECT'] = ""

from langchain_openai import ChatOpenAI


llm= ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,

)
from langchain_core.prompts import load_prompt

prompt_yaml_1 = load_prompt("Users/PC/전주대학교_인공지능학과/실무인재(겨율특강)/SUB/DATA_ALL/PROMPTTEMPLATE.YAML",)


prompt_yaml_1
prompt_yaml_1.format(fruit="사과")
chain = prompt_yaml_1 | llm