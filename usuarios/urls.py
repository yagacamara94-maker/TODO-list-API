from django.urls import path
from .views import RegistrarUsuarioView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('registro/', RegistrarUsuarioView.as_view(), name='Registar-usuário'),
    path('login/', CustomTokenObtainPairView.as_view(), name='Login-usuário'),
    path('refresh/', TokenRefreshView.as_view(), name='Refresh-token'),
]