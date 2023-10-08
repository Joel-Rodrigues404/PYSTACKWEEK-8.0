from django.shortcuts import (
    render, redirect
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import (
    TiposExames, PedidosExames,
    SolicitacaoExame,
)
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.

@login_required(login_url='usuarios:login')
def solicitar_exames(request):
    # if not request.user.is_authenticated:
    #     #pode colorar um redirect
    #     return HttpResponse("Voçe deve fazer login para acessar esta pagina")

    tipos_exames = TiposExames.objects.all()
    
    if request.method == 'GET':

        context = {
            'tipos_exames':tipos_exames
        }

        return render(request, 'solicitar_exames.html', context=context)
    elif request.method == 'POST':
        # dos dados do POST eu pego a lista de ids dos exames seleccionados no html
        exames_id = request.POST.getlist('exames')
        # exames solicitados filtrados por id na lista pega os objt
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

        # TODO verificar somente os preços dos dados disponiveis
        preco_total = 0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco
        
        context = {
            'tipos_exames':tipos_exames,
            'solicitacao_exames':solicitacao_exames,
            'preco_total':preco_total,
        }

        return render(request, 'solicitar_exames.html', context=context)

@login_required(login_url='usuarios:login')
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
    
    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )
    pedido_exame.save()
    #itera sobre um objeto django
    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario = request.user,
            exame=exame,
            status = 'E'
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
    
    pedido_exame.save()
    messages.add_message(request, messages.SUCCESS, 'Pedido de exame realizado com sucesso')

    return redirect('exames:gerenciar_pedidos')
@login_required(login_url='usuarios:login')
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    context = {
        'pedidos_exames':pedidos_exames
    }
    return render(request, 'gerenciar_pedidos.html', context=context)

@login_required(login_url='usuarios:login')
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, messages.ERROR, 'Esse pedido não e seu, portanto voçe não pode cancelar!')
        return redirect('exames:gerenciar_pedidos')
    
    pedido.agendado = False
    pedido.save()

    messages.add_message(request, messages.SUCCESS, 'Pedido cancelado com Sucesso!')
    return redirect('exames:gerenciar_pedidos')

@login_required(login_url='usuarios:login')
def gerenciar_exames(request):
    return render(request, 'gerenciar_exames.html')
