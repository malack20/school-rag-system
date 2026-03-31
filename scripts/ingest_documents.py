import os
import sys
import django

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from apps.documents.models import Document
from apps.documents.ingestion.embedding_generator import generate_embeddings_for_text

def run():
    for doc in Document.objects.all():
        generate_embeddings_for_text(doc.id, doc.text or "")

if __name__ == "__main__":
    run()
