import os
os.environ["OPENAI_API_KEY"] = "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"

from crewai import Agent

researcher = Agent(
                role="researcher",
                goal="""
                    Gather and interpret vast amounts of data to provide a comprehensive overview of the sentiment and new surrounding a stock.
                    """,
                backstory="""
                    You're skilled in gathering gathering and interpreting data from various soureces. 
                    You read each data source carefully and extract the most imprtant information. 
                    Your insights are crucial for makeing informed investment decisions.
                    """,
                verbose=True,                
            )
technical_analyst = Agent(
                role="technical analyst",
                goal="""
                    Analyze the movements of a stock and provide insights on trends, endtry points, resistance and support levels
                    """,
                backstory="""
                    An exert in technical analysis, you're known for your ability to predict stock price.
                    You provide valuable singhtes to your customers.
                    """,
                verbose=True,    
            )
financial_analyst = Agent(
                role="financial analyst",
                goal="""
                    Use financial statements, insider trading data and other metrics to evaluate a stock's financial health and performance.
                    """,
                backstory="""
                    You're a very experienced investment advisor that looks at a company's financial health, market sentiment, and qualitative data to make informed recommendations
                    """,  
                verbose=True, 
            )
hedge_fund_manager = Agent(
                role="hedge fund manager",
                goal="""
                    Manage a portfolio of stocks and make investment decisions to maximize returns using insights from financial analysts and researchers. 
                    Your answer must be in Korean.
                    Your answer must contain a detailed investment recommendation to BUY, SELL or HOLD the stock.
                    """,
                backstory="""
                    You're a seasoned hedge fund manager with a proven track record of making profitable i8nvestments.
                    You always impress your clients.
                    """,
                verbose=True,
            )

from crewai import Task

research = Task(
                description="""
                    Gather and analyze the news and makret sentiment surrounding {company}'s stock.
                    Provide a xummary of the news and andy notable shifts in sentiemnt
                """,
                agent=researcher,
                expected_output="""Your final answer MUST be a detailed summay of the news and market sentiment surrounding the stock.
                """,
                )
technical_analysis = Task(
                description="""
                    Conduct a technical analysis of the {company}' stock price movements and identify key support and resistance levels chart patterns.
                """,
                agent=technical_analyst,
                expected_output="""Your final answer MUST be a report with potential entry points, price targets and any other relevant information.
                """,
                )
financial_analysis = Task(
                description="""
                    Analyze the {company}'s financial statements, balance sheet, insider trading data and other metrics to evaluate {company}'s financial health and performance.
                """,
                agent=financial_analyst,
                expected_output="""Your final answer MUST be a report with an overview an oveview of  {company}'s revenue, earnings, cah flow, and other key financial metrics.
                """,
                )
investment_recommendation = Task(
                description="""
                    Based on the research, technical analysis and financial analysis reports, provide a detailed investment recommendation for {company}'s stock.
                """,
                Agent=hedge_fund_manager,
                expected_output="""Your final answer MUST be a detailed investment recommendation to VUY, SELL or HOLD {company}'s stock.
                Provide a clear rationle for your recommendation. 
                You must describe document in Korean.
                """,
                context=[research, technical_analysis, financial_analysis],
                output_file="4_investment_recommendation.md",
                )

from crewai_tools import tool
import yfinance as yf

@tool("Stock News")
def stock_news(ticker):
    """
    Useful to get news about a stock.
    The input should be a ticker, for example: "AAPL", "NET", "TSLA"
    """
    ticker =yf.Ticker(ticker)
    return ticker.news

from crewai_tools import ScrapeWebsiteTool

scrape_tool = ScrapeWebsiteTool()

researcher=Agent(
    role="researcher",
    goal="Gather and interpret vast amounts of data to provide a comprehensive overview of the sentiment and new surrounding a stock.",
    backstory="""You're skilled in gathering gathering and interpreting data from various soureces. 
                    You read each data source carefully and extract the most imprtant information. 
                    Your insights are crucial for makeing informed investment decisions.""",
    tools=[
        scrape_tool,
        stock_news
         ]
)

import yfinance as yf

@tool("Stock Price")
def stock_price(ticker):
    """
    Useful to get the stock price of a company.
    The input should be a ticker, for example: "AAPL", "NET", "TSLA"
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1mo")

# # 주식 가격 조회 작업을 위임하는 함수
# @tool("Stock Price Check")
# def delegate_stock_price_check(ticker):
#     task = "특정 주식의 현재 가격을 조회해주세요."
#     context = f"주식 시장에서 주식의 가격은 다양한 요인에 의해 변동됩니다. 우리는 특정 주식의 현재 가격을 알아야 합니다. 예를 들어, '{ticker}'은 해당 주식 코드입니다. 이 주식의 현재 가격을 조회해 주세요."
#     coworker = "financial analyst"
#     return task, context, coworker

technical_analyst = Agent(
    role="technical analyst",
    goal="""
                    Analyze the movements of a stock and provide insights on trends, endtry points, resistance and support levels.
                    Answer in Korean.
                    """,
                backstory="""
                    An exert in technical analysis, you're known for your ability to predict stock price.
                    You provide valuable singhtes to your customers.
                    """,
    tools=[
        stock_price,
        # delegate_stock_price_check
    ]
)

@tool("Income Statement")
def income_stmt(ticker):
    """
    Useful to get the income statement of a company.
    The input should be a ticker, for example: "AAPL", "NET", "TSLA"
    """
    ticker = yf.Ticker(ticker)
    return ticker.income_stmt

@tool("Balance Sheet")
def balance_sheet(ticker):
    """
    Useful to get the balance sheet of a company.
    The input should be a ticker, for example: "AAPL", "NET", "TSLA"
    """
    ticker = yf.Ticker(ticker)
    return ticker.balance_sheet

@tool("Insider Transactions")
def insider_transactions(ticker):
    """
    Useful to get the insider transactions of a company.
    The input should be a ticker, for example: "AAPL", "NET", "TSLA"
    """
    ticker = yf.Ticker(ticker)
    return ticker.insider_transactions

financial_analyst = Agent(
    role="financial analyst",
    goal="""
        Use financial statements, insider trading data and other metrics to evaluate a stock's financial health and performance. Answer in Korean.
        """,
    backstory="""
        You're a very experienced investment advisor that looks at a company's financial health, market sentiment, and qualitative data to make informed recommendations
        """,
    tools=[
        income_stmt,
        balance_sheet,
        insider_transactions
    ]
)

from crewai import Crew

crew = Crew(
    tasks=[research, technical_analysis, financial_analysis, investment_recommendation],
    agents=[researcher, technical_analyst, financial_analyst, hedge_fund_manager],
    verbose=True,
)


result = crew.kickoff(
    inputs={"company": "AAPL"},
)