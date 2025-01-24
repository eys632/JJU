from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# ===== 문서 로드 및 분할 =====
loader = WebBaseLoader(
    "https://teddylee777.github.io/openai/openai-assistant-tutorial/", encoding="utf-8"
)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = loader.load_and_split(text_splitter)

# ===== 벡터 DB 및 임베딩 설정 =====
openai_embedding = OpenAIEmbeddings()
db = FAISS.from_documents(docs, openai_embedding)
retriever = db.as_retriever()

# ===== MultiQueryRetriever 설정 =====
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm,
)

# ===== 문서 검색 =====
question = "OpenAI Assistant API의 Functions 사용법에 대해 알려주세요."
relevant_docs = multiquery_retriever.invoke(question)

# ===== 검색 결과 출력 =====
print(f"\n===============\n검색된 문서 개수: {len(relevant_docs)}\n===============")
print(relevant_docs[0].page_content)
print(relevant_docs[0])
