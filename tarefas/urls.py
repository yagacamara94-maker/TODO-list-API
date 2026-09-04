from django.urls import path
from .views import CreateTarefa,TarefaDetail,TarefaRetrieve

urlpatterns = [
    path(
        '',
        CreateTarefa.as_view(),
    ),
    path(
        '<int:id>/',
        TarefaDetail.as_view(),
    ),
    path(
        '<str:titulo>/',
        TarefaRetrieve.as_view()
    )
]