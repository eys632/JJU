from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader('/Users/PC/전주대학교_인공지능학과/실무인재(겨율특강)/SUB/DATA_ALL', glob="**/*.md")

docs = loader.load()

len(docs)

# loader = DirectoryLoader('./', glob="**/*.md")

docs = loader.load()

len(docs)

print(docs[0].page_content)