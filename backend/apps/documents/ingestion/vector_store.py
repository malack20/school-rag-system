import os
from typing import List
from core.constants import VECTOR_STORE_ENV_PATH

def _chroma_client():
    from chromadb import PersistentClient
    path = os.getenv(VECTOR_STORE_ENV_PATH, "./vector_store/chroma_db")
    return PersistentClient(path=path)

def _pinecone_index():
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index(os.getenv("PINECONE_INDEX", "school-rag"))

def upsert_texts(doc_id, texts, embeddings, metadatas=None):
    backend = os.getenv("VECTOR_STORE_BACKEND", "chroma").lower()
    if backend == "pinecone":
        idx = _pinecone_index()
        vectors = []
        for i, (text, emb) in enumerate(zip(texts, embeddings)):
            m = metadatas[i] if metadatas else {"doc_id": doc_id}
            m["text"] = text
            vectors.append({
                "id": f"{doc_id}-{i}",
                "values": emb,
                "metadata": m
            })
        idx.upsert(vectors=vectors)
        return

    c = _chroma_client()
    collection = c.get_or_create_collection(name="documents")
    ids = [f"{doc_id}-{i}" for i in range(len(texts))]
    if metadatas is None:
        metadatas = [{"doc_id": doc_id}] * len(texts)
    else:
        # ensure doc_id present
        for m in metadatas:
            m.setdefault("doc_id", doc_id)
    collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)

def delete_doc(doc_id):
    backend = os.getenv("VECTOR_STORE_BACKEND", "chroma").lower()
    if backend == "pinecone":
        idx = _pinecone_index()
        # Pinecone doesn't support easy delete by metadata on free tier
        # but we can at least try if supported
        try:
            idx.delete(filter={"doc_id": doc_id})
        except:
            pass
        return

    c = _chroma_client()
    collection = c.get_or_create_collection(name="documents")
    collection.delete(where={"doc_id": doc_id})
