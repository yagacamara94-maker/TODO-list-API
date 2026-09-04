from .models import Tarefa
from .serializers import CreateTarefaSerializer, UpdateTarefaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

# Create your views here.


class CreateTarefa(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = CreateTarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"mensagem":"Tarefa criada com sucesso!"},status=201)
        return Response(serializer.error_messages,status=400)

    def get(self,request):
        tarefas = Tarefa.objects.all()
        tarefaserializer = CreateTarefaSerializer(tarefas,many=True)
        return Response(tarefaserializer.data,status=200)

class TarefaDetail(APIView):
    permission_classes = [AllowAny]
    def put(self,request,id,format=None):
        tarefa = get_object_or_404(Tarefa,pk=id)
        serializer = UpdateTarefaSerializer(tarefa,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"mensagem":"Tarefa editada com sucesso!"},status=200)
        return Response(serializer.error_messages,status=400)

    def patch(self,request,id,format=None):
        tarefa = get_object_or_404(Tarefa,pk=id)
        serializer = UpdateTarefaSerializer(tarefa,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"mensagem":"Tarefa editada com sucesso!"},status=200)
        return Response(serializer.error_messages,status=400)

    def delete(self,request,id,format=None):
        tarefa = get_object_or_404(Tarefa,pk=id)
        tarefa.delete()
        return Response(data={"mensagem":"Tarefa apagada com sucesso!"})


class TarefaRetrieve(APIView):
    permission_classes = [AllowAny]

    def get(self,request,titulo):
        tarefas = Tarefa.objects.filter(titulo__icontains=titulo)
        serializer = UpdateTarefaSerializer(tarefas,many=True)
        return Response(serializer.data,status=200)