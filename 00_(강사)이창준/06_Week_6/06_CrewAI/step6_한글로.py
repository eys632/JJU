import os
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"

from crewai import Agent

## Agent 생성
researcher = Agent(
                role="연구원",
                goal="""
                    주식에 대한 감성과 뉴스를 종합적으로 파악하여 해석하는 데에 능숙합니다.
                    """,
                backstory="""
                    다양한 소스에서 데이터를 수집하고 해석하는 데에 능숙합니다.
                    각 데이터 소스를 주의 깊게 읽고 가장 중요한 정보를 추출합니다.
                    당신의 통찰력은 투자 결정에 중요합니다.
                    """,
                verbose=True,
                output_file="_research_Agent.md",       
                model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정     
            )
technical_analyst = Agent(
                role="기술 분석가",
                goal="""
                    주식의 움직임을 분석하고 추세, 진입점, 저항선 및 지지선에 대한 통찰력을 제공합니다.
                    """,
                backstory="""
                    기술적 분석에 능숙한 전문가로, 주식 가격을 예측하는 능력으로 알려져 있습니다.
                    고객들에게 가치 있는 통찰력을 제공합니다.
                    """,
                verbose=True,    
                output_file="_technical_analyst_Agent.md",
                model="gpt-3.5-turbo",
            )
financial_analyst = Agent(
                role="금융 분석가",
                goal="""
                    금융 제무제표, 내부자 거래 데이터 및 기타 지표를 사용하여 주식의 재무 건강과 성과를 평가합니다.
                    """,
                backstory="""
                    당신은 회사의 재무 건강, 시장 감성 및 질적 데이터를 고려하여 정보화된 권고를 제공하는 매우 경험 많은 투자 자문가입니다.
                    """,  
                verbose=True, 
                output_file="_financial_analyst_Agent.md",
                model="gpt-3.5-turbo",
            )
hedge_fund_manager = Agent(
                role="헤지펀드 매니저",
                goal="""
                    금융 분석가와 연구원의 통찰력을 활용하여 주식 포트폴리오를 관리하고 투자 결정을 내리는 것이 목표입니다.
                    당신의 답변은 한글로 작성되어야 합니다.
                    주식을 사야 할지, 팔아야 할지, 아니면 보유해야 할지에 대한 상세한 투자 권고를 포함해야 합니다.
                    """,
                backstory="""
                    당신은 수익성 있는 투자를 하는 데 있어 검증된 성적표를 가진 경험 많은 헤지펀드 매니저입니다.
                    항상 고객들에게 감동을 주고 있습니다.
                    """,
                verbose=True,
                output_file="_hedge_fund_manager_Agent.md",
                model="gpt-3.5-turbo",
            )

## Task 생성
from crewai import Task

research = Task(
                description="""
                    {company}의 주식에 대한 뉴스와 시장 상황을 수집하고 분석합니다.
                    뉴스의 요약과 시장상황의 주요 변화를 제공하세요.
                    """,
                agent=researcher,
                expected_output="""
                    최종 답변은 해당 주식에 대한 뉴스와 시장 감성에 대한 자세한 요약이어야 합니다.
                    """,
                output_file="1_research_Task.md",
                model="gpt-4o",
                )
technical_analysis = Task(
                description="""
                    {company}의 주식 가격 움직임에 대한 기술적 분석을 수행하고 핵심 지지선과 저항선 차트 패턴을 분석합니다.
                    """,
                agent=technical_analyst,
                expected_output="""
                    최종 답변은 잠재적인 진입점, 가격 목표 및 기타 관련 정보를 포함한 보고서여야 합니다.
                    표를 적극 활용하여 답변을 작성 합니다.
                    """,
                output_file="2_technical_analysis_Task.md",
                model="gpt-3.5-turbo",
                )
financial_analysis = Task(
                description="""
                    {company}의 재무제표, 재무상태표, 내부자 거래 데이터 및 기타 지표를 분석하여 {company}의 재무 건강과 성과를 평가합니다.
                    """,
                agent=financial_analyst,
                expected_output="""
                    최종 답변은 {company}의 매출, 이익, 현금 흐름 및 기타 주요 재무 지표에 대한 개요를 포함한 자세한 보고서여야 합니다.
                    """,
                output_file="3_financial_analysis_Task.md",
                model="gpt-3.5-turbo",
                )
investment_recommendation = Task(
                description="""
                    연구, 기술적 분석 및 재무 분석 보고서를 기반으로 {company} 주식에 대한 상세한 투자 권고를 제공하세요.
                    """,
                agent=hedge_fund_manager,
                expected_output="""
                    최종 답변은 {company} 주식에 대한 매수, 매도 또는 보유에 대한 상세한 투자 권고여야 합니다.
                    권고에 대한 명확한 이유를 제시해야 합니다.
                    답변은 동료들이 제시한 사실에 근거하여 자세히 작성되어야 합니다.
                    """,
                context=[research, technical_analysis, financial_analysis],
                output_file="4_investment_recommendation_Task.md",
                model="gpt-3.5-turbo",
                )

## Tool/Crew 생성
from crewai_tools import tool
import yfinance as yf

@tool("Stock News")
def stock_news(ticker):
    """
    특정 주식에 대한 뉴스를 가져오는 데 유용합니다.
    입력은 'ticker'여야 합니다. 예를 들어: "AAPL", "NET", "TSLA"
    """
    ticker =yf.Ticker(ticker)
    return ticker.news

from crewai_tools import ScrapeWebsiteTool

scrape_tool = ScrapeWebsiteTool()

researcher=Agent(
    role="연구원",
    goal="""
        주식에 대한 감성과 뉴스를 종합적으로 파악하여 해석하는 데에 능숙합니다.
        """,
    backstory="""
        다양한 소스에서 데이터를 수집하고 해석하는 데에 능숙합니다.
        각 데이터 소스를 주의 깊게 읽고 가장 중요한 정보를 추출합니다.
        당신의 통찰력은 투자 결정에 중요합니다.
        """,
    tools=[
        scrape_tool,
        stock_news
        ],
    model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
    # output_file="_researcher_Agent.md"
)

import yfinance as yf

@tool("Stock Price")
def stock_price(ticker):
    """
    특정 회사의 주식 가격을 가져오는 데 유용합니다.
    입력은 'ticker'여야 합니다. 예를 들어: "AAPL", "NET", "TSLA"
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1mo")

technical_analyst = Agent(
    role="기술 분석가",
    goal="""
        주식의 움직임을 분석하고 추세, 진입점, 저항선 및 지지선에 대한 통찰력을 제공합니다.
        답변은 한글로 작성되어야 합니다.
        """,
    backstory="""
        기술적 분석에 능숙한 전문가로, 주식 가격을 예측하는 능력으로 알려져 있습니다.
        고객들에게 가치 있는 통찰력을 제공합니다.
        """,
    tools=[
        stock_price,
        # delegate_stock_price_check
    ],
    model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
)

@tool("Income Statement")
def income_stmt(ticker):
    """
    회사의 손익계산서를 가져오는 데 유용합니다.
    입력은 'ticker'여야 합니다. 예를 들어: "AAPL", "NET", "TSLA"
    """
    model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
    ticker = yf.Ticker(ticker)
    return ticker.income_stmt

@tool("Balance Sheet")
def balance_sheet(ticker):
    """
    회사의 재무상태표를 가져오는 데 유용합니다.
    입력은 'ticker'여야 합니다. 예를 들어: "AAPL", "NET", "TSLA"
    """
    model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
    ticker = yf.Ticker(ticker)
    return ticker.balance_sheet

@tool("Insider Transactions")
def insider_transactions(ticker):
    """
    회사의 내부자 거래 데이터를 가져오는 데 유용합니다.
    입력은 'ticker'여야 합니다. 예를 들어: "AAPL", "NET", "TSLA"
    """
    ticker = yf.Ticker(ticker)
    model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
    return ticker.insider_transactions

financial_analyst = Agent(
    role="금융 분석가",
    goal="""
        금융 제무제표, 내부자 거래 데이터 및 기타 지표를 사용하여 주식의 재무 건강과 성과를 평가합니다.
        답변은 한글로 작성되어야 합니다.
        """,
    backstory="""
        당신은 회사의 재무 건강, 시장 감성 및 질적 데이터를 고려하여 정보화된 권고를 제공하는 매우 경험 많은 투자 자문가입니다.
        """,
    tools=[
        income_stmt,
        balance_sheet,
        insider_transactions
    ],
    model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
)

## Crew 생성
from crewai import Crew

crew = Crew(
    tasks=[research, technical_analysis, financial_analysis, investment_recommendation],
    agents=[researcher, technical_analyst, financial_analyst, hedge_fund_manager],
    # model="gpt-3.5-turbo",
    verbose=True,
)


result = crew.kickoff(
    inputs={"company": "AAPL"},
    # model="gpt-3.5-turbo",  # 접근 가능한 모델로 설정  
)
