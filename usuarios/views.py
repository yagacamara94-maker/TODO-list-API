from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import create_user_serializer

# Create your views here.

class RegistrarUsuarioView(generics.CreateAPIView):
    serializer_class = create_user_serializer
    permission_classes = [AllowAny]