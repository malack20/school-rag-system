import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

def _llm():
    try:
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        return ChatOpenAI(api_key=api_key, model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"), temperature=0.2)
    except Exception:
        return None

def _vectorstore():
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    persist_directory = os.getenv("VECTOR_STORE_PATH", "./vector_store/chroma_db")
    return Chroma(collection_name="documents", embedding_function=embeddings, persist_directory=persist_directory)

def run_langchain_pipeline(query: str) -> str:
    vs = _vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 5})
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="Answer the question using the context.\nContext:\n{context}\nQuestion:\n{question}\nAnswer:"
    )
    llm = _llm()
    if llm is None:
        # Fallback: just return empty to allow upstream to handle fallback
        return ""
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    resp = chain.invoke(query)
    try:
        return resp.content if hasattr(resp, "content") else str(resp)
    except Exception:
        return str(resp)
