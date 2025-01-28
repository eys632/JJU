# Setup------------------------------------------
# 0.0 API 키를 환경변수로 관리하기 위한 설정 파일
import os
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

# 0.1 LangSmith 로깅 설정
from newstool import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("ls_JJU_Agent_01")

# print(os.environ['OPENAI_API_KEY'])
# ------------------------------------------------


# Code Start--------------------------------------

from langchain.tools import tool
from typing import List, Dict, Annotated
from newstool.news import GoogleNews
from newstool.tavily import TavilySearch
from langchain_experimental.utilities import PythonREPL
import json


# 1.1 도구 생성
@tool
def search_news(query: str) -> List[Dict[str, str]]:
    """
    Search Google News by input keyword
    Always answer in Korean.
    Make a markdown file with the result in same-path with name 'search.md'
    """
    news_tool = GoogleNews()  # 튜플이 아닌 객체로 정의
    # output="search.md" 
    # news_tool = TavilySearch()
    return news_tool.search_by_keyword(query, k=5)

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user. Always answer in Korean.
    Make a markdown file with the result in same-path with name 'code.md'. """
    result = ""
    try:
        result = PythonREPL().run(code),
        # output = "code.md"
    except BaseException as e:
        print(f"Failed to execute. Error: {repr(e)}")
    finally:
        return result


# 1.2 도구 정의
tools = [search_news, python_repl_tool]

from langchain_core.prompts import ChatPromptTemplate

# 2. 프롬프트 생성
## 프롬프트는 에이전트에게 모델이 수행할 작업을 설명하는 텍스트를 제공합니다. (도구의 이름과 역할을 입력)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "Make sure to use the `search_news` tool for searching keyword related news.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent

# 3. LLM 정의
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 4. Agent 생성
agent = create_tool_calling_agent(llm, tools, prompt)

from langchain.agents import AgentExecutor

# 5. Agent 실행 툴: AgentExecutor 생성
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    max_execution_time=10,
    handle_parsing_errors=True,
)

# 6. AgentExecutor 실행
result = agent_executor.invoke({"input": "AI"})

# 7. AgentExecutor 결과 출력: 뉴스 헤더만 출력
print("뉴스 헤더:")
print(result["output"])