# Setup------------------------------------------
# 0.0 API 키를 환경변수로 관리하기 위한 설정 파일
import os
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

# 0.1 LangSmith 로깅 설정
from newstool import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("ls_JJU_langGraph_01")

# print(os.environ['OPENAI_API_KEY'])
# ------------------------------------------------

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

## State 정의
class State(TypedDict):
    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)
    messages: Annotated[list, add_messages]  

from langchain_openai import ChatOpenAI

## Node 정의
llm = ChatOpenAI(model = "gpt-4o", temperature = 0)

def chatbot(state:State):
    return {"messages":[llm.invoke(state["messages"])]}

## graph 정의
graph_builder = StateGraph(State)

## 노드 추가
graph_builder.add_node("chatbot", chatbot)
# graph_builder.add_node("chatbot_2", chatbot)

## 엣지 추가
graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", "chatbot_2")
# graph_builder.add_edge("chatbot_2", "chatbot")
graph_builder.add_edge("chatbot", END)

## 그래프 컴파일
graph = graph_builder.compile()

## 그래프 시각화
from graphs.graphs import visualize_graph_mermaid

visualize_graph_mermaid(graph_builder)

## 그래프 실행
query = "서울의 맛집 추천?"

# 그래프 이벤트 스트리밍
for event in graph.stream({"messages": [("user", query)]}):
    # 이벤트 값 출력
    for value in event.values():
        print("Assistant:", value["messages"][-1].content)


from newstool.messages import display_message_tree

# 메타데이터(tree 형태로 출력)
# display_message_tree(snapshot.metadata)

display_message_tree(State)