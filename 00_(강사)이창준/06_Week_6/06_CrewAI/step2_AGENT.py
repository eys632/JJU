import os
os.environ["OPENAI_API_KEY"] = "sk-proj-oUpwqlbDGPJb0H3NOT2MT3BlbkFJgDEFOReLR0QNaVfCNoQ6"

from crewai import Agent

researcher = Agent()
technical_analyst = Agent()
financial_analyst = Agent()
hedge_fund_manager = Agent()
