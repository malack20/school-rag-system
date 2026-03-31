from rest_framework.views import APIView
from rest_framework.response import Response
from .analytics import get_summary

class AnalyticsView(APIView):
    def get(self, request):
        return Response(get_summary())
