from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import create_user_serializer, customserializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RegistrarUsuarioView(generics.CreateAPIView):
    serializer_class = create_user_serializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = customserializer