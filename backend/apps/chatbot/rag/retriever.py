import os
from core.constants import VECTOR_STORE_ENV_PATH
from apps.documents.models import Document

def _chroma_client():
    try:
        from chromadb import PersistentClient
        path = os.getenv(VECTOR_STORE_ENV_PATH, "./vector_store/chroma_db")
        return PersistentClient(path=path)
    except Exception:
        # Chroma might not be available in all environments; fall back to in-db search.
        return None

def _pinecone_query(query: str, n_results: int):
    try:
        import pinecone
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX", "school-rag")
        if not api_key:
            return []
        pinecone.init(api_key=api_key, environment=os.getenv("PINECONE_ENV", ""))
        idx = pinecone.Index(index_name)
        # For brevity, we assume embeddings computed elsewhere and use server-side sparse search if available
        # In a real setup, we would embed 'query' and query by vector
        return []  # Placeholder
    except Exception:
        return []

def _fast_fallback(query: str):
    q = (query or "").lower()
    keys = [w for w in q.split() if len(w) > 3][:3]
    texts = []
    for doc in Document.objects.all()[:20]:
        t = (doc.text or "")
        if any(k in t.lower() for k in keys):
            parts = [p.strip() for p in t.split("\n\n") if p.strip()]
            texts.extend(parts[:2])
        if len(texts) >= 5:
            break
    return texts[:5] if texts else [t[:500] for t in [doc.text or ""]]

def retrieve_chunks(query: str):
    backend = os.getenv("VECTOR_STORE_BACKEND", "chroma").lower()
    if backend == "pinecone":
        return _pinecone_query(query, n_results=5)
    c = _chroma_client()
    if c is None:
        return _fast_fallback(query)
    collection = c.get_or_create_collection(name="documents")
    try:
        results = collection.query(query_texts=[query], n_results=3)
        docs = results.get("documents", [[]])[0]
        if docs:
            return docs
    except Exception:
        pass
    return _fast_fallback(query)

def retrieve_chunks_with_meta(query: str):
    backend = os.getenv("VECTOR_STORE_BACKEND", "chroma").lower()
    if backend == "pinecone":
        # Placeholder: return empty meta
        return [], []
    c = _chroma_client()
    if c is None:
        texts = _fast_fallback(query)
        metas = [{"doc_id": None}] * len(texts)
        return texts, metas
    collection = c.get_or_create_collection(name="documents")
    try:
        results = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas"])
        docs = results.get("documents", [[]])[0] or []
        metas = results.get("metadatas", [[]])[0] or []
        if docs:
            return docs, metas
    except Exception:
        pass
    # Fallback: build from heuristic
    texts = _fast_fallback(query)
    metas = [{"doc_id": None}] * len(texts)
    return texts, metas
