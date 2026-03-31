from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UsersView(APIView):
    def get(self, request):
        qs = User.objects.all()
        return Response(UserSerializer(qs, many=True).data)
