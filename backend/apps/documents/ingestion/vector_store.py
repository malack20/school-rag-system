import os
from typing import List
from core.constants import VECTOR_STORE_ENV_PATH

def _chroma_client():
    from chromadb import PersistentClient
    path = os.getenv(VECTOR_STORE_ENV_PATH, "./vector_store/chroma_db")
    return PersistentClient(path=path)

def upsert_texts(doc_id, texts, embeddings, metadatas=None):
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
    c = _chroma_client()
    collection = c.get_or_create_collection(name="documents")
    collection.delete(where={"doc_id": doc_id})
