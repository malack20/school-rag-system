from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DocumentSerializer
from .models import Document
from .ingestion.embedding_generator import generate_embeddings_for_text
from .ingestion.loader import extract_text
from .ingestion.vector_store import delete_doc
from .services.analysis_service import analyze_text
from rest_framework.permissions import AllowAny
from .ingestion.metadata_extractor import extract_sections

class DocumentListView(APIView):
    def get(self, request):
        qs = Document.objects.order_by("-uploaded_at")
        return Response(DocumentSerializer(qs, many=True).data)

class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        s = DocumentSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        doc = s.save()
        text = extract_text(doc.file.path)
        doc.text = text
        doc.save()
        generate_embeddings_for_text(doc.id, text)
        return Response(DocumentSerializer(doc).data, status=201)

class ReindexView(APIView):
    def post(self, request):
        for doc in Document.objects.all():
            generate_embeddings_for_text(doc.id, doc.text or "")
        return Response({"status": "ok"})

class DocumentDeleteView(APIView):
    def delete(self, request, id):
        try:
            doc = Document.objects.get(id=id)
        except Document.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        delete_doc(doc.id)
        doc.delete()
        return Response(status=204)

class AnalyzeDocumentView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request, id):
        try:
            doc = Document.objects.get(id=id)
        except Document.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        feedback = analyze_text(doc.text or "")
        structured = extract_sections(doc.text or "")
        return Response({"id": doc.id, "title": doc.title, "feedback": feedback, "structured": structured})

class ExtractDocumentView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request, id):
        try:
            doc = Document.objects.get(id=id)
        except Document.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        structured = extract_sections(doc.text or "")
        return Response({"id": doc.id, "title": doc.title, "structured": structured})
