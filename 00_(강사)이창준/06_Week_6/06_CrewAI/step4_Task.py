import os
os.environ["OPENAI_API_KEY"] = ""

from crewai import Agent

researcher = Agent(
                role="researcher",
                goal="""
                    Gather and interpret vast amounts of data to provide a comprehensive overview of the sentiment and new surrounding a stock.
                    """,
                backstory="""
                    You're skilled in gathering gathering and interpreting data from various soureces. 
                    You read each data source carefully and extract the most imprtant information. 
                    Your insights are crucial for makeing informed investment decisions
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
                    """,
                backstory="""
                    You're a seasoned hedge fund manager with a proven track record of making profitable i8nvestments.
                    You always impress your clients.
                    """,
                verbose=True,
            )

from crewai import tasks

research = tasks(
                description="""
                    Gather and analyze the news and makret entiment surrounding {company}'s stock.
                    Provide a xummary of the news and andy notable shifts in sentiemnt
                """,
                agent=researcher,
                expected_output="""Your final answer MUST be a detailed summay of the news and market sentiment surrounding the stock.
                """,
                )
technical_analysis = tasks(
                description="""
                    Conduct a technical analysis of the {company}' stock price movements and identify key support and resistance levels chart patterns.
                """,
                agent=technical_analyst,
                expected_output="""Your final answer MUST be a report with potential entry points, price targets and any other relevant information.
                """,
                )
financial_analysis = tasks(
                description="""
                    Analyze the {company}'s financial statements, balance sheet, insider trading data and other metrics to evaluate {company}'s financial health and performance.
                """,
                agent=financial_analyst,
                expected_output="""Your final answer MUST be a report with an overview an oveview of  {company}'s revenue, earnings, cah flow, and other key financial metrics.
                """,
                )

investment_recommendation = tasks(
                description="""
                    Based on the research, technical analysis and financial analysis reports, provide a detailed investment recommendation for {company}'s stock.
                """,
                Agent=hedge_fund_manager,
                expected_output="""Your final answer MUST be a detailed investment recommendation to VUY, SELL or HOLD {company}'s stock.
                Provide a clear rationle for your recommendation.
                """,
                context=[research, technical_analysis, financial_analysis],
                output_file="investment_recommendation.md",
                )

