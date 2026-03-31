from django.urls import path
from .views import ChatView, ChatLogsView, ChatAnswerView

urlpatterns = [
    path("", ChatView.as_view()),
    path("logs", ChatLogsView.as_view()),
    path("answer", ChatAnswerView.as_view()),
]
