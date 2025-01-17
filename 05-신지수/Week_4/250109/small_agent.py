import os
from langchain.agents import Tool, AgentExecutor, initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

os.environ["OPENAI_API_KEY"] = "API 키"
os.environ["LANGCHAIN_API_KEY"] = "API 키"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "test_JJU_ShinJisoo"

#------------------------------------------------------------------------------------

def simba_Agent(research_instr, summarize_instr):
    search = DuckDuckGoSearchRun()
    
    tools = [
        Tool(
            name="Internet Search",
            func=search.run,
            description="Useful for searching information on the internet"
        )
    ]
    
    llm = ChatOpenAI(temperature=0)
    
    research_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    
    # Create a chain for summarization
    summarize_chain = load_summarize_chain(llm, chain_type="stuff")
    
    try:
        # Execute research
        research_result = research_agent.run(research_instr)
        
        # Summarize the research results
        summary = summarize_chain.run(research_result)
        
        return summary
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

research_instr = input('어떤 주제를 검색하고 싶은지 질문해주세요: ')
summarize_instr = input('검색한 내용을 어떤식으로 요약하길 원하는지 답변해주세요: ')

result = simba_Agent(research_instr, summarize_instr)
if result:
    print("\n결과:\n", result)