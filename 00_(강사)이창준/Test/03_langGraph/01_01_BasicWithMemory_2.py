# Setup------------------------------------------
# 0.0 API 키를 환경변수로 관리하기 위한 설정 파일
import os
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

# 0.1 LangSmith 로깅 설정
from newstool import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("ls_JJU_langGraph_01_01")


# MemorySaver 생성
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# Graph 생성 ------------------------------------------------------------------------
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from newstool.tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


########## 1. 상태 정의 ##########
# 상태 정의
class State(TypedDict):
    # 메시지 목록 주석 추가
    messages: Annotated[list, add_messages]


########## 2. 도구 정의 및 바인딩 ##########
# 도구 초기화
tool = TavilySearch(max_results=3)
tools = [tool]

# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini")

# 도구와 LLM 결합
llm_with_tools = llm.bind_tools(tools)


########## 3. 노드 추가 ##########
# 챗봇 함수 정의
def chatbot(state: State):
    # 메시지 호출 및 반환
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# 상태 그래프 생성
graph_builder = StateGraph(State)

# 챗봇 노드 추가
graph_builder.add_node("chatbot", chatbot)

# 도구 노드 생성 및 추가
tool_node = ToolNode(tools=[tool])

# 도구 노드 추가
graph_builder.add_node("tools", tool_node)

# 조건부 엣지
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

########## 4. 엣지 추가 ##########

# tools > chatbot
graph_builder.add_edge("tools", "chatbot")

# START > chatbot
graph_builder.add_edge(START, "chatbot")

# chatbot > END
graph_builder.add_edge("chatbot", END)

# --------------------------------------------------------------------------------------------

# 그래프 빌더 컴파일
graph = graph_builder.compile(checkpointer=memory)

from graphs.graphs import visualize_graph

# 그래프 시각화
visualize_graph(graph)



# RunnableConfig 설정 -------------------------------------------------------------------------
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    recursion_limit=10,  # 최대 10개의 노드까지 방문. 그 이상은 RecursionError 발생
    configurable={"thread_id": "1"},  # 스레드 ID 설정
)

# 첫 질문
question = (
    "내 이름은 `테디노트` 입니다. YouTube 채널을 운영하고 있어요. 만나서 반가워요"
)

for event in graph.stream({"messages": [("user", question)]}, config=config):
    for value in event.values():
        value["messages"][-1].pretty_print()
        
from langchain_core.runnables import RunnableConfig

question = "내 이름이 뭐라고 했지?"

config = RunnableConfig(
    recursion_limit=10,  # 최대 10개의 노드까지 방문. 그 이상은 RecursionError 발생
    configurable={"thread_id": "1"},  # 스레드 ID 설정
)

for event in graph.stream({"messages": [("user", question)]}, config=config):
    for value in event.values():
        value["messages"][-1].pretty_print()
        
# Snapshot --------------------------------------------------------------------------------------------
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    configurable={"thread_id": "1"},  # 스레드 ID 설정
)
# 그래프 상태 스냅샷 생성
snapshot = graph.get_state(config)
snapshot.values["messages"]

# 설정된 config 정보
snapshot.config

# 저장된 값(values)
snapshot.values

# 다음 노드
snapshot.next

snapshot.metadata["writes"]["chatbot"]["messages"][0]

# 노드 시각화 -------------------------------------------------------------------------------------------
from newstool.messages import display_message_tree

# 메타데이터(tree 형태로 출력)
display_message_tree(snapshot.metadata)