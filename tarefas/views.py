from .models import Tarefa
from .serializers import CreateTarefaSerializer, UpdateTarefaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.


class CreateTarefa(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = CreateTarefaSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"mensagem":"Tarefa criada com sucesso!"},status=201)
        return Response(serializer.error_messages,status=400)

    def get(self,request):
        tarefas = Tarefa.objects.filter(usuario=request.user.id)
        tarefaserializer = CreateTarefaSerializer(tarefas,many=True)
        return Response(tarefaserializer.data,status=200)

class TarefaDetail(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,id):
        tarefa = get_object_or_404(Tarefa,pk=id,usuario=request.user.id)
        serializer = UpdateTarefaSerializer(tarefa,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"mensagem":"Tarefa editada com sucesso!"},status=200)
        return Response(serializer.error_messages,status=400)

    def patch(self,request,id):
        tarefa = get_object_or_404(Tarefa,pk=id,usuario=request.user.id)
        serializer = UpdateTarefaSerializer(tarefa,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"mensagem":"Tarefa editada com sucesso!"},status=200)
        return Response(serializer.error_messages,status=400)

    def delete(self,request,id):
        tarefa = get_object_or_404(Tarefa,pk=id,usuario=request.user.id)
        tarefa.delete()
        return Response(data={"mensagem":"Tarefa apagada com sucesso!"})


class TarefaRetrieve(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,titulo):
        tarefas = Tarefa.objects.filter(titulo__icontains=titulo,usuario=request.user.id)
        serializer = UpdateTarefaSerializer(tarefas,many=True)
        return Response(serializer.data,status=200)