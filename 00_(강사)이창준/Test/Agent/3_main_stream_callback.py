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

from langchain.tools import tool
from typing import List, Dict, Annotated
from newstool.news import GoogleNews
from newstool.tavily import TavilySearch
from langchain_experimental.utilities import PythonREPL
import json


# # 1.1 도구 생성
@tool
def search_news(query: str) -> List[Dict[str, str]]:
    """Search Google News by input keyword"""
    news_tool = GoogleNews()
    # news_tool = TavilySearch()
    return news_tool.search_by_keyword(query, k=5)

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    result = ""
    try:
        result = PythonREPL().run(code)
    except BaseException as e:
        print(f"Failed to execute. Error: {repr(e)}")
    finally:
        return result


# # 1.2 도구 정의
tools = [search_news, python_repl_tool]

from langchain_core.prompts import ChatPromptTemplate

# # 2. 프롬프트 생성
# ## 프롬프트는 에이전트에게 모델이 수행할 작업을 설명하는 텍스트를 제공합니다. (도구의 이름과 역할을 입력)
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

# # 3. LLM 정의
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# # 4. Agent 생성
agent = create_tool_calling_agent(llm, tools, prompt)

from langchain.agents import AgentExecutor

# # 5. Agent 실행 툴: AgentExecutor 생성
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    max_execution_time=10,
    handle_parsing_errors=True,
)

# # ---------------------
# # 8. Stremam Parser
# # ---------------------

# from newstool.messages import AgentStreamParser

# agent_stream_parser = AgentStreamParser()

# # 질의에 대한 답변을 스트리밍으로 출력 요청
# result = agent_executor.stream(
#     # {"input": "인공지능의 최신 뉴스를 검색하세요."}
#     {"input": """
#      matplotlib 을 사용하여 titanic.dataset을 이용하여 연령별 탑승인원을 시각화 해.
#      10살 단위로 pie 차트를 그리는 코드를 작성하고 실행하세요.
#      """}
# )

# for step in result:
#     # 중간 단계를 parser 를 사용하여 단계별로 출력
#     # print(step)
#     # print("=====================================")
#     agent_stream_parser.process_agent_steps(step)

# AgentCallbacks와 AgentStreamParser를 langchain_teddynote.messages에서 가져옵니다.
from newstool.messages import AgentCallbacks, AgentStreamParser


# 도구 호출 시 실행되는 콜백 함수입니다.
def tool_callback(tool) -> None:
    print("<<<<<<< 도구 호출 >>>>>>")
    print(f"Tool: {tool.get('tool')}")  # 사용된 도구의 이름을 출력합니다.
    # st.markdown(f"### {tool.get('tool')}")  # 사용된 도구의 이름을 출력합니다.
    print("<<<<<<< 도구 호출 >>>>>>")


# 관찰 결과를 출력하는 콜백 함수입니다.
def observation_callback(observation) -> None:
    print("<<<<<<< 관찰 내용 >>>>>>")
    print(
        f"Observation: {observation.get('observation')[0]}"
    )  # 관찰 내용을 출력합니다.
    # st.markdown(f"### {observation.get('observation')[0]}")  # 관찰 내용을 출력합니다.
    print("<<<<<<< 관찰 내용 >>>>>>")


# 최종 결과를 출력하는 콜백 함수입니다.
def result_callback(result: str) -> None:
    print("<<<<<<< 최종 답변 >>>>>>")
    print(result)  # 최종 답변을 출력합니다.
    # st.markdown(f"### {result}")  # 최종 답변을 출력합니다.
    print("<<<<<<< 최종 답변 >>>>>>")


# AgentCallbacks 객체를 생성하여 각 단계별 콜백 함수를 설정합니다.
agent_callbacks = AgentCallbacks(
    tool_callback=tool_callback,
    observation_callback=observation_callback,
    result_callback=result_callback,
)

# AgentStreamParser 객체를 생성하여 에이전트의 실행 과정을 파싱합니다.
agent_stream_parser = AgentStreamParser(agent_callbacks)

# 질의에 대한 답변을 스트리밍으로 출력 요청
result = agent_executor.stream({"input": "대한민국의 정치상황을 알려 줘."})

for step in result:
    # 중간 단계를 parser 를 사용하여 단계별로 출력
    agent_stream_parser.process_agent_steps(step)