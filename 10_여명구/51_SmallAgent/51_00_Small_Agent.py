import os
from dotenv import load_dotenv
from praisonaiagents import Agent, Agents, Tools

load_dotenv()  # .env 파일 로드
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user_input = input("Enter your question in Korean: ")

# 리서치 에이전트 정의
research_agent = Agent(
    instructions=f"You are a research agent tasked to search the internet about the question: '{user_input}'. You must show the search process and respond in Korean.",
    tools=[Tools.internet_search],
    api_key=OPENAI_API_KEY,
    # lim='gpt-4o',
)

# 요약 에이전트 정의
summarize_agent = Agent(
    instructions="You are a summarize agent. Your task is to summarize the research agent's findings and provide the summary in Korean.",
    api_key=OPENAI_API_KEY,
    # lim='gpt-4o',
)

agents = Agents(agents=[research_agent, summarize_agent])
agents.start()