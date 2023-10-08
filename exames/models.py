from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TiposExames(models.Model):
    TIPO_CHOICES = (
        ('I','Exame de imagem'),
        ('S','Exame de Sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self) -> str:
        return self.nome
    
class SolicitacaoExame(models.Model):    
    CHOICE_STATUS = (
        ('E', 'Em análise'),        
        ('F', 'Finalizado')
    )    
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)    
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)    
    status = models.CharField(max_length=2, choices=CHOICE_STATUS)  
    # onde sera armazenado o pdf com o resultado do exame que sera salva em uma pasta resultados  
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)# Null e blank definem que n e nesseçario o resultado para salvar este modelo  
    requer_senha = models.BooleanField(default=False)    
    senha = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):        
        return f'{self.usuario} | {self.exame.nome}'
    
class PedidosExames(models.Model):    
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)    
    #               de muitos pra muitos
    exames = models.ManyToManyField(SolicitacaoExame)    
    agendado = models.BooleanField(default=True)    
    data = models.DateField()    
    
    def __str__(self):        
        return f'{self.usuario} | {self.data}'