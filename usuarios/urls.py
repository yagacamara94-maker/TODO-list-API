from django.urls import path
from .views import RegistrarUsuarioView

urlpatterns = [
    path('registro/',RegistrarUsuarioView.as_view(),name='Registar-usuário'),
]