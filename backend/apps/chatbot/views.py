from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatMessageSerializer
from .models import ChatMessage
from .services.chat_service import generate_response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import AllowAny
from apps.documents.models import Document
from .rag.retriever import retrieve_chunks_with_meta
from .rag.prompt_template import build_prompt
from .rag.response_generator import generate_answer

class ChatView(APIView):
    def post(self, request):
        s = ChatMessageSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        content = s.validated_data["content"]
        reply = generate_response(content)
        msg = ChatMessage.objects.create(user=request.user if request.user.is_authenticated else None, content=content, response=reply)
        return Response(ChatMessageSerializer(msg).data, status=201)

class ChatLogsView(APIView):
    def get(self, request):
        qs = ChatMessage.objects.order_by("-created_at")[:200]
        return Response(ChatMessageSerializer(qs, many=True).data)

class ChatAnswerView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        content = request.data.get("content", "")
        docs, metas = retrieve_chunks_with_meta(content)
        prompt = build_prompt(content, docs)
        reply = generate_answer(prompt)
        sources = []
        for i, m in enumerate(metas):
            doc_id = m.get("doc_id") if isinstance(m, dict) else None
            title = None
            if doc_id:
                try:
                    d = Document.objects.get(id=doc_id)
                    title = d.title
                except Document.DoesNotExist:
                    title = None
            sources.append({
                "doc_id": doc_id,
                "title": title,
                "snippet": (docs[i] if i < len(docs) else "")[:300],
            })
        return Response({"response": reply, "sources": sources})
