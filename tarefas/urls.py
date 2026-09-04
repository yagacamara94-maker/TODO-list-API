from django.urls import path
from .views import CreateTarefa,TarefaDetail,TarefaRetrieve

urlpatterns = [
    path(
        '',
        CreateTarefa.as_view(),
        name='List-Create'
    ),
    path(
        '<int:id>/',
        TarefaDetail.as_view(),
        name='Update-Delete'
    ),
    path(
        '<str:titulo>/',
        TarefaRetrieve.as_view(),
        name='Retrieve'
    )
]