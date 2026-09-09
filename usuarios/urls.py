from django.urls import path
from .views import RegistrarUsuarioView,CustomTokenObtainPairView

urlpatterns = [
    path('registro/',RegistrarUsuarioView.as_view(),name='Registar-usuário'),
    path('login/',CustomTokenObtainPairView.as_view(),name='Login-usuário')
]