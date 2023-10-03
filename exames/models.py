from django.db import models

# Create your models here.

class TipoExames(models.Model):
    
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self) -> str:
        return self.nome