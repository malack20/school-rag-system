from django.urls import path
from .views import DocumentListView, DocumentUploadView, ReindexView, DocumentDeleteView, AnalyzeDocumentView, ExtractDocumentView

urlpatterns = [
    path("", DocumentListView.as_view()),
    path("upload", DocumentUploadView.as_view()),
    path("reindex", ReindexView.as_view()),
    path("<int:id>/delete", DocumentDeleteView.as_view()),
    path("<int:id>/analyze", AnalyzeDocumentView.as_view()),
    path("<int:id>/extract", ExtractDocumentView.as_view()),
]
