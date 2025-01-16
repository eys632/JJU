from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

output_parser = CommaSeparatedListOutputParser()

format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template = "List five{subject}.\n{format_instructions}",
    input_valiables = ["subject"],
    partial_variables = {"format_instructions" : format_instructions}
)

model = ChatOpenAI(temperature = 0)

chain = prompt | model | output_parser

response = chain.invoke({"subject": "미국에서 인구 수가 많은 주 순서"})
print(response)