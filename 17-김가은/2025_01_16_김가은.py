from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

output_parser = CommaSeparatedListOutputParser()

format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],  
    partial_variables={"format_instructions": format_instructions},
)

model = ChatOpenAI(temperature=0)
chain = prompt | model | output_parser

prompt
response = chain.invoke({"subject": "한국인이 좋아하는 아이스크림"})
