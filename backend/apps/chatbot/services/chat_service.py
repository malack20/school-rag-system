import os
from ..rag.rag_pipeline import run_pipeline
from ..rag.langchain_pipeline import run_langchain_pipeline

def generate_response(query):
    if os.getenv("USE_LANGCHAIN", "0") == "1":
        ans = run_langchain_pipeline(query)
        if ans:
            return ans
    return run_pipeline(query)
