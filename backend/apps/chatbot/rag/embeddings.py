from sentence_transformers import SentenceTransformer
from core.constants import DEFAULT_EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(DEFAULT_EMBEDDING_MODEL)
    return _model

def embed_texts(texts):
    model = get_model()
    return model.encode(texts).tolist()
