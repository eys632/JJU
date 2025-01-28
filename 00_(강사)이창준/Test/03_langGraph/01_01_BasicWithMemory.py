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

# print(os.environ['OPENAI_API_KEY'])
# ------------------------------------------------

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

## State 정의
class State(TypedDict):
    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)
    messages: Annotated[list, add_messages]  

from langchain_openai import ChatOpenAI
from newstool.tavily import TavilySearch

## Memory 정의
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

## tool 정의
tool = TavilySearch(max_results=5)
tools=[tool]

## Node 정의
llm = ChatOpenAI(model = "gpt-4o", temperature = 0)
llm_with_tools=llm.bind_tools(tools)

def chatbot(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

## graph 정의
graph_builder = StateGraph(State)

# 도구 노드 생성 및 추가
tool_node = ToolNode(tools=[tool])

## 노드 추가
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
# graph_builder.add_node("chatbot_2", chatbot)


## 조건부 엣지 추가
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

## 엣지 추가
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")
# graph_builder.add_edge("chatbot", "chatbot_2")
# graph_builder.add_edge("chatbot_2", "chatbot")
graph_builder.add_edge("chatbot", END)

## 그래프 컴파일
graph = graph_builder.compile()

## 그래프 시각화
from graphs.graphs import visualize_graph_mermaid

visualize_graph_mermaid(graph_builder)

## Config 설정
from graphs.config  import RunnableConfig

config = RunnableConfig(
    reculsion_limit=10,
    configurable={'thread_id': "1", 'timeout': 60},
)

## 그래프 재 컴파일
graph = graph_builder.compile(checkpointer=memory)

## 그래프 실행
query = "서울의 맛집 추천?"

config = RunnableConfig(
    configurable={'thread_id': '1', 'timeout': 60},
)

# 그래프 이벤트 스트리밍
for event in graph.stream({"messages": [("user", query)]},config=config):
    # 이벤트 값 출력
    for value in event.values():
        print("Assistant:", value["messages"][-1].pretty_print())


print('before display_message_tree(State)')
from newstool.messages import display_message_tree

# 메타데이터(tree 형태로 출력)
# display_message_tree(snapshot.metadata)

display_message_tree(graph)

print('after display_message_tree(State)')

##### Config Visualize #######


config = RunnableConfig(
    configurable={'thread_id': '1', 'timeout': 60},
)

snapshot = graph.get_state(config)

# print('snapshot.config')
(snapshot.config).pretty_print()
# print('snapshot.values')
(snapshot.values).pretty_print()
# print('snapshot.metadata')
(snapshot.metadata).pretty_print()
