from django.urls import path
from .views import CreateTarefa,TarefaDetail

urlpatterns = [
    path(
        '',
        CreateTarefa.as_view(),
    ),
    path(
        '<int:id>/',
        TarefaDetail.as_view(),
    ),
]