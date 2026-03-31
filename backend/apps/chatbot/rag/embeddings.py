import os
from openai import OpenAI

_client = None

def get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def embed_texts(texts):
    client = get_client()
    # Use OpenAI's text-embedding-3-small for cost and memory efficiency
    response = client.embeddings.create(
        input=texts,
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )
    return [data.embedding for data in response.data]
