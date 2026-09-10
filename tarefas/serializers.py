from .models import Tarefa
from rest_framework import serializers

class CreateTarefaSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Tarefa
        fields = ['id','titulo', 'status','data_criacao','usuario']
        read_only_fields = ['id','data_criacao']

    def validate_titulo(self, titulo):
        titulo = titulo.strip()
        if not titulo:
            raise serializers.ValidationError("O título não pode ser em branco!")
        elif len(titulo) < 3:
            raise serializers.ValidationError("O título não pode ter menos de três caracteres!")
        elif len(titulo) > 200:
            raise serializers.ValidationError("O título não pode ter mais de duzentos caracteres!")
        return titulo

    def validate_status(self,status):
        if status != "P":
            raise serializers.ValidationError("O status da tarefa só pode ser editado após a sua criação!")
        return status

class UpdateTarefaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tarefa
        fields = ['id','titulo', 'status','data_criacao']
        read_only_fields = ['id','data_criacao']

    def validate_titulo(self, titulo):
            titulo = titulo.strip()
            if not titulo:
                raise serializers.ValidationError("O título não pode ser em branco!")
            elif len(titulo) < 3:
                raise serializers.ValidationError("O título não pode ter menos de três caracteres!")
            elif len(titulo) > 200:
                raise serializers.ValidationError("O título não pode ter mais de duzentos caracteres!")
            return titulo

    def validate_status(self,status):
        if status not in ['P','A','F']:
            raise serializers.ValidationError("Status inválido!")
        return status




    

    
        
