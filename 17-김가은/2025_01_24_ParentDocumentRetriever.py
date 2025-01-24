
!pip install langchain-community langchain-chroma langchain-openai

from langchain_community.document_loaders import TextLoader

loaders = [
    # 파일을 로드합니다.
    TextLoader("/content/appendix-keywords.txt"),
]

docs = []
for loader in loaders:
    # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.
    docs.extend(loader.load())

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 자식 분할기를 생성합니다.
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

# DB를 생성합니다.
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=OpenAIEmbeddings()
)

store = InMemoryStore()

# Retriever 를 생성합니다.
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
)

from langchain_openai import OpenAIEmbeddings
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma

# DB를 생성합니다.
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=OpenAIEmbeddings()
)

store = InMemoryStore()

from langchain.retrievers import ParentDocumentRetriever


retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
)

# 문서를 검색기에 추가합니다. docs는 문서 목록이고, ids는 문서의 고유 식별자 목록입니다.
retriever.add_documents(docs, ids=None, add_to_docstore=True)

# 저장소의 모든 키를 리스트로 반환합니다.
list(store.yield_keys())

# 유사도 검색을 수행합니다.
sub_docs = vectorstore.similarity_search("Word2Vec")

# sub_docs 리스트의 첫 번째 요소의 page_content 속성을 출력합니다.
print(sub_docs[0].page_content)

# 문서를 검색하여 가져옵니다.
retrieved_docs = retriever.invoke("Word2Vec")

# 검색된 문서의 문서의 페이지 내용의 길이를 출력합니다.
print(
    f"문서의 길이: {len(retrieved_docs[0].page_content)}",
    end="\n\n=====================\n\n",
)

# 문서의 일부를 출력합니다.
print(retrieved_docs[0].page_content[2000:2500])

# 부모 문서를 생성하는 데 사용되는 텍스트 분할기입니다.
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
# 자식 문서를 생성하는 데 사용되는 텍스트 분할기입니다.
# 부모보다 작은 문서를 생성해야 합니다.
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)
# 자식 청크를 인덱싱하는 데 사용할 벡터 저장소입니다.
vectorstore = Chroma(
    collection_name="split_parents", embedding_function=OpenAIEmbeddings()
)
# 부모 문서의 저장 계층입니다.
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    # 벡터 저장소를 지정합니다.
    vectorstore=vectorstore,
    # 문서 저장소를 지정합니다.
    docstore=store,
    # 하위 문서 분할기를 지정합니다.
    child_splitter=child_splitter,
    # 상위 문서 분할기를 지정합니다.
    parent_splitter=parent_splitter,
)

retriever.add_documents(docs)  # 문서를 retriever에 추가합니다.

















