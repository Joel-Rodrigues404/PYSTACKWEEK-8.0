from django.shortcuts import (render, redirect)
from django.http import (HttpResponse)
from django.contrib.auth.models import (User)
from django.contrib.messages import (constants)
from django.contrib import (messages)
from django.contrib.auth import (authenticate, login, logout)
# Create your views here.


def cadastro(request):

    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        # Captura o valor dos campos quando o metodo e POST
        # nome_var    = request.POST.get('atributo name= no html')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # TODO passar para um arquivo de utils 
        #Validaçoes de dados

        if not senha == confirmar_senha:
            # messages.adicionar_mensagem(request>para saber pra qual user vai ser a msg, tipo da mensagem, mensagem de fato)
            messages.add_message(request, constants.ERROR, 'As senhas Não são iguais!')
            return redirect('usuarios:cadastro')
        
        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, 'A senha não pode ter menos que 8 digitos!')
            return redirect('usuarios:cadastro')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, 'Nome de Usuario ja existe!')
            return redirect('usuarios:cadastro')
        # TODO validar se o username do usuario não existe
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password = senha
            )
            messages.add_message(request, constants.SUCCESS, 'Usuario criado com sucesso!')
        except:
            messages.add_message(request, constants.ERROR, 'Erro Interno do sistema contate um Administrador')
            return redirect('usuarios:cadastro')

        return HttpResponse('passou salvo ')

def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        #verifica as credenciais, validar se o usuario tem o username e a senha cadastradas no database
        user = authenticate(username=username, password=senha)
        
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Username ou senha invalidos')
            return redirect('usuarios:login')
            


