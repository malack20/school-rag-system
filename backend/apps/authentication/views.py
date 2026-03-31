import secrets
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import AuthToken

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        data = s.validated_data
        if User.objects.filter(username=data["username"]).exists():
            return Response({"detail": "Username taken"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data["username"], email=data["email"], password=data["password"]
        )
        token = AuthToken.objects.create(user=user, key=secrets.token_hex(32))
        return Response({"user": UserSerializer(user).data, "token": token.key}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        s = LoginSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        data = s.validated_data
        username = data.get("username", "") or ""
        email = data.get("email")
        if email and not username:
            try:
                from django.contrib.auth.models import User as U
                u = U.objects.get(email=email)
                username = u.username
            except U.DoesNotExist:
                username = ""
        user = authenticate(username=username, password=data["password"])
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = AuthToken.objects.get_or_create(user=user, defaults={"key": secrets.token_hex(32)})
        return Response({"user": UserSerializer(user).data, "token": token.key}, status=200)
