import os
os.environ["OPENAI_API_KEY"] = ""

from crewai import Agent

researcher = Agent()
technical_analyst = Agent()
financial_analyst = Agent()
hedge_fund_manager = Agent()
