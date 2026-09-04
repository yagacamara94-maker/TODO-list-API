from django.db import models

# Create your models here.

class Tarefa(models.Model):

    status_choices = [
        ("P", "PENDENTE"),
        ("A", "ANDAMENTO"),
        ("F", "FEITO"),
    ]

    titulo = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=status_choices, default='P')
    data_criacao = models.DateField(auto_now_add=True, editable=False)
