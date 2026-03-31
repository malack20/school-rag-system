from .text_splitter import split_text
from .vector_store import upsert_texts
from apps.chatbot.rag.embeddings import embed_texts
from .metadata_extractor import classify_section

def generate_embeddings_for_text(doc_id, text):
    chunks = split_text(text or "")
    if not chunks:
        return
    vecs = embed_texts(chunks)
    metas = [{"doc_id": doc_id, "section": classify_section(c)} for c in chunks]
    upsert_texts(doc_id, chunks, vecs, metas)
